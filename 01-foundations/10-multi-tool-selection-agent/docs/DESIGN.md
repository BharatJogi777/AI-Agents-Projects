# AG-010 design notes — Multi-tool selection agent

## Responsibility split

The LLM is a planner/selector: it interprets the request and proposes one or more calls from the schemas supplied to it. The Python process is the execution authority: it owns the registry, validates arguments, applies resource limits, calls handlers, and decides whether the run may continue.

This distinction matters. A tool schema is not a security boundary by itself. The registry lookup and validation in Python are the enforcement boundary.

## Request lifecycle

1. The CLI creates one long-lived HTTPX-backed Ollama client.
2. `MultiToolAgent.run` validates the user prompt and its UTF-8 byte length.
3. The agent sends the conversation and the fixed tool definitions to Ollama.
4. If the model returns no tool calls, the agent validates that the final answer is non-empty and within the output byte limit.
5. If tool calls are returned, the agent checks the per-step call limit and preserves the assistant message in the conversation.
6. Each call is parsed, looked up in the local registry, validated using its Pydantic model, and executed.
7. The result is serialized to bounded JSON and appended as a tool message. If the provider supplied a call ID, the response carries the same ID.
8. The model is called again, until it answers or the configured step limit is reached.

## Why multiple tools can be called in one turn

The model may return an array of calls, for example an addition request and a text-length request. The agent executes each call independently and appends one result per call. A configured upper bound prevents a single response from triggering an unbounded number of operations.

The current handlers are local and read-only except for reading the system clock. If future tools mutate external systems, they need explicit authorization, idempotency, audit records, and often human approval; the model's choice is not user authorization.

## Registry contract

Each entry contains:
- a stable tool name,
- a Pydantic argument model,
- a Python handler,
- a concise description sent to the model.

The model cannot register tools or change their schemas. Extra fields are forbidden. The arithmetic tool accepts finite values within a bounded range. The text tool has a maximum input length. The time tool validates an IANA timezone through `zoneinfo`.

## Resource limits

| Resource | Default |
|---|---:|
| Model steps | 4 |
| Tool calls per step | 4 |
| Prompt UTF-8 bytes | 32,000 |
| Tool-result UTF-8 bytes | 8,000 |
| Final-answer UTF-8 bytes | 8,000 |
| Provider request timeout | 60 seconds |

These are learning-project defaults, not universal production values. Tune them for model context size, latency, expected tool cost, and deployment quotas.

## Error policy

- Malformed model envelopes fail the run.
- Unknown tools and invalid arguments become generic tool errors, without reflecting submitted values.
- Tool implementation exceptions are logged by the application and returned as a generic failure.
- Provider timeout/HTTP failures fail fast; the agent does not silently retry potentially expensive model requests.
- Exhausting the model-step budget ends the run.

## Threat model and limitations

The model and its output are untrusted. Prompt injection can influence which available tool it proposes and what arguments it supplies. Schema validation prevents malformed inputs, but does not determine whether a requested operation is appropriate for a particular user. This sample therefore exposes only low-impact local tools.

Before adding a privileged tool:
1. Authenticate the caller independently of the model.
2. Authorize the caller for the specific operation and resource.
3. Validate resource identifiers and enforce tenant boundaries.
4. Add idempotency for mutations and audit events for consequential actions.
5. Add approval checkpoints where the risk warrants them.
6. Bound execution time, output size, concurrency, and external spend.

No authentication, persistence, tenant isolation, cancellation, distributed tracing, or human approval is included here. Tests are authored but not executed in the maintainer's environment.

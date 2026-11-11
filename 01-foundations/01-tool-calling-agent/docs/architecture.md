# Architecture

| Component | Responsibility | Must not do |
|---|---|---|
| API / CLI | Accept input and return output | Decide which tools are trusted |
| ToolCallingAgent | Own the bounded model/tool loop | Execute arbitrary model-provided code |
| ChatClient protocol | Define provider boundary | Contain business tool implementations |
| OllamaChatClient | Translate messages to Ollama HTTP and normalize provider failures | Authorize tool use |
| Tool allowlist | Dispatch explicitly registered functions | Dynamically import model-selected modules |
| Pydantic models | Validate tool arguments | Treat valid input as authorized intent |

## Request lifecycle

1. CLI/API validates the user prompt.
2. Agent builds a conversation with trusted system instructions.
3. Model receives registered tool schemas.
4. Proposed tool name is looked up in the local allowlist.
5. Pydantic validates arguments before execution.
6. Deterministic Python handler returns a result.
7. Result is appended as a tool message.
8. Model receives the tool result and writes a final answer or the step budget is exhausted.

The model proposes actions. Python owns validation, authorization, execution, and limits.

## Health model

- Liveness (`/health/live`) answers whether the API process can respond.
- Readiness (`/health/ready`) checks the configured Ollama model through `/api/tags`; it does not run inference.
- A readiness failure should remove the instance from service without restarting a healthy process.

## Provider HTTP behavior

The adapter reuses one `httpx.Client` to benefit from connection pooling. It applies explicit request/connect timeouts, validates the minimum response contract, and maps provider failures to sanitized application errors. It deliberately does not retry: retry policy belongs around a request/agent step, where idempotency and remaining run budget can be considered.

## Trust boundaries

User input, model output, and tool output are untrusted. The local allowlist is the authority for executable capabilities. Dependency injection lets tests replace the provider with a deterministic fake or MockTransport-backed HTTP client.

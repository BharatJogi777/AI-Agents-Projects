# Design notes

## Component boundaries

- `SchemaRepairAgent` owns the generation/validation/repair state machine.
- `StructuredGenerator` is a protocol; the agent does not depend on Ollama or HTTPX.
- `OllamaClient` implements the protocol and sends the Pydantic JSON Schema through Ollama's native `format` field.
- `TaskReport` is the application contract. Strict Pydantic validation rejects coercion and unknown fields.

## Retry semantics

`max_retries` counts repairs after the initial generation. The maximum number of model calls is `1 + max_retries`; configuration is capped at three repairs. Only output-contract failures are repairable: malformed/schema-invalid JSON, empty content, and output beyond configured limits. Provider/network exceptions propagate immediately. Network retry/backoff belongs in a separate transport policy.

## Input and output boundaries

The request is JSON-encoded before it is placed in the user message. This prevents request text from escaping XML-like prompt delimiters, although JSON framing is not a prompt-injection defence. The model must still be treated as untrusted and tool authorization must remain deterministic application logic.

Both character and UTF-8 byte limits are applied to output. The request has a UTF-8 byte limit. A rejected response is returned to the model only as bounded untrusted conversation data so it can be corrected; it is never promoted to a trusted instruction. Validation feedback omits Pydantic input values, caps the number of errors, truncates field paths/messages, and has a total size limit.

## Acceptance and observability

Only strict schema-valid `TaskReport` values are returned. Exhaustion raises `SchemaRepairExhausted`; the last invalid payload is never returned. Logs contain attempt metadata and failure categories, not request text or model output. The exception message is safe for CLI display; its `last_error` field contains bounded schema diagnostics and should not be exposed to end users without review.

## Operational boundaries

The adapter uses a persistent HTTPX client with a request timeout and sanitized transport errors. The CLI closes the client in a `finally` block. Add request-scoped correlation IDs, metrics, provider rate limits, circuit breaking, and semantic evaluation before production use. A schema-valid result can still be factually incorrect; schema repair is not grounding or human approval.

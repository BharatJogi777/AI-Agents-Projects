# Architecture and trust boundaries

## Components

| Component | Responsibility |
|---|---|
| CLI (`app/main.py`) | Parse user input and compose dependencies |
| StructuredOutputAgent | Build trusted instructions, request schema-constrained generation, enforce byte limits, validate output |
| StructuredGenerator protocol | Provider-independent contract for structured generation |
| OllamaClient | Translate the contract into Ollama's native `/api/chat` request |
| TaskAnalysis | Pydantic contract consumed by downstream application code |

## Request lifecycle

1. The CLI loads configuration and creates the Ollama adapter.
2. The agent rejects empty or oversized user input before making a network call.
3. The agent builds a system instruction and frames the user's text as untrusted data.
4. The Pydantic model exports a JSON Schema.
5. Ollama receives that schema in the native `format` field with streaming disabled and temperature zero.
6. The adapter validates the provider response envelope and returns only the message content.
7. The agent enforces an output byte limit.
8. Pydantic parses and validates the response with strict validation and unknown fields forbidden.
9. Only the typed `TaskAnalysis` object is returned to the caller.

## Important distinction

JSON Schema constrains output shape. Pydantic verifies that shape again at the application boundary. Neither proves that the model's claims are true. Factual grounding requires source evidence and a separate verification step.

## Failure behavior

- Provider timeout or connection failure: fail the request; no unvalidated result is returned.
- Provider HTTP error: raise a sanitized error without echoing the response body.
- Missing or empty `message.content`: reject the provider response.
- Oversized input or output: reject before expensive parsing or further processing.
- Invalid JSON, enum, or unknown field: raise `OutputValidationError`.
- No silent fallback to free-form text is allowed.

## Extension points

Inject a different `StructuredGenerator` for another provider or deterministic tests. Keep provider-specific HTTP details out of the agent and keep business decisions out of the LLM adapter.

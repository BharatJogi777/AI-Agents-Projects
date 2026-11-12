# Architecture and validation boundaries

## Component responsibilities

| Component | Responsibility | Must not do |
|---|---|---|
| CLI composition root | Load settings, construct adapter and agent, print typed result | Contain extraction rules |
| StructuredOutputAgent | Bound input/output, build messages, call generator, validate result | Trust raw model JSON |
| StructuredGenerator protocol | Define provider-independent structured generation contract | Contain business rules |
| OllamaClient | Map messages and JSON Schema to Ollama `/api/chat`; normalize transport errors | Decide whether extracted facts are true |
| TaskAnalysis / ActionItem | Define strict output contract and field constraints | Perform network calls |
| Evidence validator | Check source quote provenance and owner/date quote support | Claim semantic correctness |

## Request sequence

1. CLI receives the original request text.
2. Agent rejects blank or oversized input before any model request.
3. Agent sends a trusted task instruction and the request as untrusted data.
4. Ollama receives the generated JSON Schema in its `format` field.
5. Agent enforces a maximum response byte size.
6. Pydantic rejects malformed JSON, unknown keys, invalid enums, and invalid field combinations.
7. Evidence validation requires each action's quote to be an exact substring of the original input.
8. If owner or due date is extracted, its own evidence quote must contain that value and also be an exact source substring.
9. Only the validated Pydantic object is returned to the caller.

## Trust boundaries

- The model is an untrusted generator, not a validator.
- User text is untrusted input and must not override the system task.
- JSON Schema is a generation constraint, not an application security boundary.
- Pydantic validation is deterministic but cannot establish factual truth.
- Exact evidence matching establishes provenance, not entailment.

## Failure behavior

The agent fails closed: invalid JSON, invalid schema, oversized output, fabricated evidence, or unsupported owner/date values raise `OutputValidationError`. No partially validated object is returned.

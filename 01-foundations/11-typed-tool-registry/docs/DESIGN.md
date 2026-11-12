# Design notes — AG-011

## Responsibility boundary

The registry owns the mapping from a provider-visible name to a trusted handler and a strict argument model. It does not decide whether a particular user is authorized to invoke a tool, nor does it implement the LLM loop. This separation keeps model planning outside the execution trust boundary.

## Registration lifecycle

Registration is an application-startup operation. Names use a constrained lowercase identifier grammar, descriptions and tool counts are bounded, argument models must be Pydantic model classes, and handlers must be callable. The application calls `freeze()` once configuration is complete. A frozen registry cannot be changed by runtime model output.

## Invocation lifecycle

- Unknown names fail closed.
- Arguments must be mapping/object values; arrays, strings, and scalars are rejected.
- Pydantic strict validation rejects coercion and extra fields when the model uses `extra="forbid"`.
- Handler exceptions are wrapped in a stable public error. The original exception remains chained for trusted internal diagnostics but its message is not exposed.
- Handler results are encoded as finite JSON, checked against a UTF-8 byte limit, then decoded to return a detached JSON-compatible value. This prevents accidental non-JSON objects, NaN/Infinity, mutable object leakage, and oversized outputs from crossing the registry boundary.

## Provider schemas

Schemas are generated from Pydantic and copied through JSON serialization before being returned. A caller can modify its copy without changing registry state. Provider schema support differs; callers may need provider-specific adaptation. The local registry always revalidates arguments regardless of provider-side validation.

## Failure handling

`ToolRegistrationError` indicates a configuration defect and should fail application startup. `ToolExecutionError` is a safe invocation-level error suitable for controlled handling by an agent loop. Callers should log the exception chain in a protected channel with appropriate redaction; do not send stack traces or internal exception text to the model.

## Non-goals and production integration

This package does not sandbox Python handlers. It does not supply authentication, per-user authorization, network policies, timeouts, concurrency limits, cancellation, rate limiting, idempotency, or durable audit logs. Those are execution-runtime responsibilities. Side-effecting tools should have explicit authorization and idempotency contracts before being exposed to an agent.

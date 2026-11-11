# Security notes and deployment gate

This is a local learning reference, not a public multi-tenant service.

## Implemented controls

- Explicit tool allowlist; no shell, filesystem, browser, or arbitrary Python execution.
- Pydantic validation for tool arguments.
- Bounded model-step count and provider HTTP timeout.
- API prompt length and unknown-field validation.
- Generic public API errors.

## Required before production exposure

1. Authenticate callers and authorize each tool per tenant/user.
2. Add rate limits, concurrency limits, deadlines, and per-user cost budgets.
3. Add durable run state, idempotency, cancellation, and audit retention.
4. Use network egress controls and a secret manager.
5. Add retry classification, circuit breaking, metrics, and tracing.
6. Keep prompts and secrets out of logs and trace attributes.
7. Add human approval for consequential side effects.
8. Run dependency, container, and threat-model reviews.

The API has no built-in authentication. Keep it on localhost or behind a trusted gateway until authentication and authorization exist.

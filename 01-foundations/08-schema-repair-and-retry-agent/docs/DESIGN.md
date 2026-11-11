# Design notes

## Retry semantics

`max_retries` counts repairs after the initial model call. Therefore the maximum number of calls is `1 + max_retries`. Configuration is capped at three repairs.

## Retry classification

Pydantic validation failures, empty responses, and responses over the configured character limit are treated as output-contract failures and can be repaired. Transport and provider exceptions are not retried by this layer. Network retry/backoff is a separate resilience concern and should have its own policy.

## Feedback minimization

The feedback contains at most ten validation errors with bounded messages and field paths. It deliberately excludes submitted values, which may contain secrets or personal data. The raw invalid response is still part of the model conversation for correction, but is length-capped and treated as untrusted content.

## Acceptance

Only a response that passes strict Pydantic validation is returned. Exhaustion raises an exception with attempt count and a short failure category; no invalid result is silently accepted.

## Further hardening

Production deployments should add request-scoped correlation IDs, structured metrics for attempt counts, provider timeouts, rate limits, output redaction policies, and regression evaluation for repair success and semantic correctness.

# AG-017 — Retry with exponential backoff

A bounded synchronous retry primitive for transient failures. It uses exponential backoff, bounded jitter, an optional server-provided retry delay, and a total elapsed-time budget.

## Safety model

- The first operation attempt always runs.
- Further attempts require explicit `idempotent=True`. A retry can repeat a request whose first response was lost after the server committed its side effect.
- By default, only `ConnectionError` and `TimeoutError` are retryable. Use `retry_if` for a narrow provider-specific allowlist (for example, selected HTTP 429/503 responses).
- Never classify validation, authentication, authorization, or permanent business errors as transient.
- Use an idempotency key at the remote service for side-effecting requests; a local boolean cannot guarantee remote deduplication.
- The operation must return or raise promptly. This synchronous helper cannot interrupt a blocked call; configure connect/read/total timeouts in the HTTP or database client too.

## Backoff calculation

For retry number n (first retry n=0):

`ceiling = min(max_delay, base_delay * multiplier ** n)`

A symmetric jitter factor is applied using an injected random source. The final delay is clamped to `max_delay`. If `retry_after` returns a delay, the larger of the calculated delay and server delay is used, still capped by `max_delay`.

## Example

```python
from retry_policy import RetryPolicy, retry

result = retry(
    lambda: payment_client.get_status("payment-123"),
    policy=RetryPolicy(max_attempts=4, base_delay=0.2, max_delay=2.0, max_elapsed=5.0),
    idempotent=True,
)
```

For a side-effecting POST, use a stable idempotency key and classify only known transient responses:

```python
result = retry(
    lambda: payment_client.create_payment(payload, idempotency_key="order-123"),
    policy=RetryPolicy(max_attempts=3),
    idempotent=True,
    retry_if=lambda exc: isinstance(exc, TemporaryGatewayError),
)
```

## Layout

- `retry_policy/policy.py`: immutable validated policy and exhaustion error.
- `retry_policy/retry.py`: execution, classification, delay calculation, and time budget.
- `tests/test_retry.py`: deterministic tests with injected sleep, clock, and random source.
- `app.py`: backward-compatible facade.

## Run locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

No network service is required. Tests are authored in the repository; run them locally to verify in your environment.

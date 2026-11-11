# AG-017 — Retry with exponential backoff

A bounded synchronous retry primitive with exponential delay, jitter, an injectable sleeper/random source, and explicit exhaustion errors.

## Architecture
- `retry_policy/policy.py`: immutable validated attempt/delay/jitter settings and exhaustion exception.
- `retry_policy/retry.py`: retry classifier, bounded exponential schedule, jitter, and operation execution.
- `app.py`: compatibility facade.

## Execution flow
1. Execute the operation once.
2. If it fails, consult the optional `retry_if` classifier.
3. Stop immediately for non-retryable failures.
4. Otherwise compute capped exponential backoff and bounded jitter.
5. Raise `RetryExhausted` after the final attempt, preserving the original cause.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Retries can duplicate side effects. Use only for idempotent operations or supply an idempotency key; classify transient errors explicitly in production. The default retries all ordinary Exceptions for tutorial convenience. Local test execution remains pending.

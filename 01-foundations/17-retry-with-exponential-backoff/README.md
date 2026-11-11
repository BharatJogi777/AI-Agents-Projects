# AG-017 — Retry with exponential backoff

A small retry primitive applies bounded exponential delays with symmetric jitter, supports a caller-defined retry predicate, and preserves the final exception as the cause of a typed exhaustion error. Sleep and randomness are injectable for deterministic tests.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Retry only transient/idempotent operations. Do not blindly retry writes or non-idempotent tool calls; use idempotency keys and classify provider errors. Always combine retries with an overall request deadline. Local test execution is pending.

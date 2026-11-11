# AG-043 — Idempotent tool execution

An idempotency key is bound to a canonical JSON fingerprint. Repeated matching requests replay the stored result; changed payloads conflict.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

The example cache is in-memory. Real side effects require a durable idempotency record and the side effect to commit atomically.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

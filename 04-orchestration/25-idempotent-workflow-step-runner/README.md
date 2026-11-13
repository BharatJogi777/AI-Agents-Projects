# Idempotent workflow step runner

Prevent duplicate step execution using stable idempotency keys and cached successful results.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Production considerations
These implementations demonstrate orchestration semantics in one process. Real distributed workflows need transactional persistence, durable event logs, idempotent external APIs, timeouts, observability, and explicit policies for partial compensation failures.

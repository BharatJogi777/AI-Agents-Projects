# Saga-style agent workflow

Coordinate a sequence of distributed-style steps with compensating actions and a durable execution record.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Production considerations
These implementations demonstrate orchestration semantics in one process. Real distributed workflows need transactional persistence, durable event logs, idempotent external APIs, timeouts, observability, and explicit policies for partial compensation failures.

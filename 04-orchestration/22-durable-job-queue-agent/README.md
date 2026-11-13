# Durable job queue agent

Implement a SQLite-backed job queue with atomic claiming, persisted attempts, and completion state.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Production considerations
This is an educational in-process reference. Production workers need durable leases, dead-letter handling, idempotent side effects, observability, bounded resource use, and a shared transactional backend where multiple processes coordinate.

# AG-034 — Plan execution tracker

Tracks each task through PENDING, RUNNING, SUCCEEDED, FAILED, and SKIPPED states. It gates task start on successful dependencies, supports explicit retry after failure, and makes terminal completion idempotent.

## Modules
- `plan_tracker/contracts.py`: status enum and mutable per-step state.
- `plan_tracker/tracker.py`: locked state transitions, dependency checks, and snapshots.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The tracker is in-memory and process-local. It is not a durable workflow engine: persist state transitions transactionally and use leases/outbox patterns before coordinating workers. Local test execution remains pending.
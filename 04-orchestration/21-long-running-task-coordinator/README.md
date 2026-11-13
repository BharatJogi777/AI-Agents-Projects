# Long-running task coordinator

Track long-running tasks through explicit states, leases, heartbeats, and bounded retries.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Production considerations
This is an educational in-process reference. Production workers need durable leases, dead-letter handling, idempotent side effects, observability, bounded resource use, and a shared transactional backend where multiple processes coordinate.

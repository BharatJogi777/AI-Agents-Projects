# Compensating action workflow

Run ordered actions and execute registered compensations in reverse order after a failure.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Production considerations
This is an educational in-process reference. Production workers need durable leases, dead-letter handling, idempotent side effects, observability, bounded resource use, and a shared transactional backend where multiple processes coordinate.

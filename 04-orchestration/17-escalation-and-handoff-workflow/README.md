# Escalation and handoff workflow

Escalate unresolved tasks to a named owner using bounded levels and an auditable handoff record.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Design notes
Uses injected handlers for deterministic testing. In production, authenticate owners, persist audit events, use idempotency keys for side effects, and protect workflow state. This is an in-process reference implementation, not a distributed workflow engine.

# Checkpointed workflow agent

Execute sequential workflow steps and persist snapshots so progress can be inspected and resumed.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Design notes
Uses injected handlers for deterministic testing. In production, authenticate owners, persist audit events, use idempotency keys for side effects, and protect workflow state. This is an in-process reference implementation, not a distributed workflow engine.

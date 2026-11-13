# Hierarchical agent team

Validate a bounded delegation tree and execute leaf workers before aggregating parent results.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Design

- `app/hierarchy.py`: deterministic orchestration core.
- `tests/test_hierarchy.py`: success and failure-path coverage.

The implementation keeps agent decisions behind injected callables so orchestration is independently testable. For production, add durable state, deadlines, cancellation, idempotency, structured audit events, and distributed coordination. Treat model-generated plans and outputs as untrusted input and validate them before side effects.

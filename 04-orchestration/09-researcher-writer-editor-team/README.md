# Researcher-writer-editor team

Pass sourced findings through drafting and editing stages while preserving provenance and checking required citations.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Design

- `app/editorial.py`: deterministic orchestration core.
- `tests/test_editorial.py`: success and failure-path coverage.

The implementation keeps agent decisions behind injected callables so orchestration is independently testable. For production, add durable state, deadlines, cancellation, idempotency, structured audit events, and distributed coordination. Treat model-generated plans and outputs as untrusted input and validate them before side effects.

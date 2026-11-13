# Human-in-the-loop approval graph

Pause a workflow for an explicit approval decision before executing a protected action.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Design notes
The implementation uses injected callables so orchestration logic can be tested without an LLM provider. Persist workflow state before irreversible side effects, make external actions idempotent, authenticate reviewers, and retain audit records in production. This example is an in-process reference, not a distributed workflow engine.

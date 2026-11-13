# Parallel task executor

Execute independent tasks concurrently with bounded workers and collect task-scoped failures.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Design

- `app/executor.py`: deterministic orchestration primitive.
- `tests/test_executor.py`: normal and failure-path tests.

The core deliberately does not depend on an LLM framework. Keep planning/model calls behind an adapter and validate all proposed steps, tools, and arguments before execution. Add durable state, distributed locks, deadlines, cancellation propagation, tracing, and idempotency before using this in a multi-process production service. The included executor is a local reference implementation, not a distributed scheduler.

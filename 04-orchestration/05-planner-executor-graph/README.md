# Planner-executor graph

Validate a bounded dependency plan, execute ready nodes, and stop dependent nodes after failed prerequisites.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Design
- `app/plan.py`: plan validation, dependency-cycle detection, deterministic execution.
- `tests/test_plan.py`: dependency, failure, cycle, and invalid-reference cases.

The core deliberately does not depend on an LLM framework. Keep model planning behind an adapter and validate all proposed steps, tools, and arguments before execution. Add durable state, deadlines, cancellation, tracing, idempotency, and distributed scheduling before production use.

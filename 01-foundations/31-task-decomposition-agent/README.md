# AG-031 — Task decomposition agent

Turns a goal into a bounded dependency graph. The planner is injected; application code owns validation, duplicate detection, dependency integrity, cycle detection, and topological ordering.

## Modules
- `task_decomposer/contracts.py`: immutable task DTO.
- `task_decomposer/validator.py`: validates IDs/descriptions/dependencies and detects cycles.
- `task_decomposer/agent.py`: planner boundary and objective/task limits.
- `app.py`: compatibility facade for the original tutorial imports.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The returned tasks are dependency-first. The planner is not allowed to execute them. Persist the graph and pass it through AG-033 validation before execution. Model-backed planning and local test execution remain pending.
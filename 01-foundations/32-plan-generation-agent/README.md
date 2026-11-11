# AG-032 — Plan generation agent

Generates a typed, bounded execution plan through an injected planner and provides strict deterministic JSON serialization/deserialization.

## Modules
- `plan_generator/contracts.py`: immutable plan and step DTOs.
- `plan_generator/agent.py`: planner boundary and objective/step/field validation.
- `plan_generator/serialization.py`: stable JSON output and strict input shape, duplicate-ID, and size checks.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Plan generation does not authorize actions. Feed the plan into AG-033 before execution. Model-backed planning and local test execution remain pending.
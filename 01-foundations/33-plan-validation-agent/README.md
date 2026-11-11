# AG-033 — Plan validation agent

A deterministic pre-execution policy gate. Validates bounded step count, unique IDs, action length, allowed risk, dependency references, and acyclic graph structure. Valid plans include a dependency-first topological order.

## Modules
- `plan_validator/contracts.py`: step and validation result DTOs.
- `plan_validator/validator.py`: policy and graph validation.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This validates structure and configured risk labels, not the real-world safety of an action. Enforce authorization and human approval separately. Local test execution remains pending.
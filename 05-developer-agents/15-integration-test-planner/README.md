# Integration Test Planner

Builds a dependency-aware integration test matrix from declared service boundaries. It identifies success, timeout, and downstream failure scenarios while leaving execution to the owning team.

## Run
```bash
pip install -e ".[dev]"
python -m app.integration_plan
pytest
```

## Limitations
It does not discover infrastructure or call services. Supply real service names and contracts; verify environment isolation and cleanup before running generated scenarios.

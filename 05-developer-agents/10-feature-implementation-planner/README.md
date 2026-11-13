# Feature Implementation Planner

Creates a staged engineering plan for a feature request: discovery, design, implementation slices, verification, rollout, and rollback. The plan is intentionally generic where repository-specific evidence is unavailable.

## Run
```bash
pip install -e ".[dev]"
python -m app.feature_plan
pytest
```

## Design and limitations
The planner uses explicit feature scope and constraints supplied by the caller. It does not pretend to inspect a repository, estimate effort, or infer hidden requirements. Human review is required before committing to scope or rollout.

# AG-180: Dynamic team composition agent

## Purpose
Builds a bounded team of available agents that covers a required capability set, using a deterministic greedy weighted set-cover heuristic.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
The planner validates agent identities, costs, availability, and team-size bounds. It selects the next agent by newly covered required capabilities relative to cost, then stable tie-breakers. It fails explicitly when coverage or size constraints cannot be met.

## Production considerations
Persist agent availability and reserve capacity atomically in a shared store before dispatch. Revalidate capabilities at execution time, add policy constraints, and record selection rationale for auditability. This is a local planning primitive, not a distributed scheduler.

Tests are authored but must be executed in the target environment before deployment.
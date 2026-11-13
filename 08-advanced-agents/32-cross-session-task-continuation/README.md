# Cross Session Task Continuation

Validate persisted task snapshots and determine whether a task can safely resume in a new session.

## Safety boundary
This reference implementation operates only on supplied data. It does not access external accounts, execute tasks, or infer missing facts.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

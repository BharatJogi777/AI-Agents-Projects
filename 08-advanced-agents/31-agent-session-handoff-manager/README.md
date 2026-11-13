# Agent Session Handoff Manager

Create a portable, validated handoff packet containing task state, constraints, decisions, and pending work.

## Safety boundary
This reference implementation operates only on supplied data. It does not access external accounts, execute tasks, or infer missing facts.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

# Agent red-team scenario runner

**Project ID:** AG-436

## Purpose
Run repeatable, bounded adversarial scenarios against an agent adapter and report failures without executing dangerous actions.

## Design
- Deterministic Python library; no external model/API dependency.
- Accepts explicit evaluation data so results are reproducible and auditable.
- Validates inputs and reports structured results rather than silently coercing invalid data.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

## Scope and limitations
This is an evaluation component, not a production safety guarantee. Integrate it with a controlled test adapter, retain raw evidence under your organization's data policy, and review thresholds before using results for release decisions.

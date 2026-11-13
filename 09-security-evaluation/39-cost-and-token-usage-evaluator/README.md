# Cost and token usage evaluator

**Project ID:** AG-439

## Purpose
Aggregate token usage and estimate model cost from explicit per-million token rates, with input validation and budget flags.

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

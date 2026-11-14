# AG-452 — Source credibility assessor

## Purpose
A deterministic, testable component for the research and knowledge-work lifecycle. It operates only on explicitly supplied inputs; it does not browse, fabricate citations, or assert that heuristic output is ground truth.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
- Pure Python domain logic with immutable result objects.
- Validates inputs and makes assumptions or limitations visible.
- No network access, credentials, external side effects, or automatic publication.
- Human review is required before relying on research conclusions.

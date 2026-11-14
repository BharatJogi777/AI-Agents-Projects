# Experiment design assistant

## Purpose
Create a structured, reviewable experiment plan from a research question, measurable outcome, and caller-defined constraints. It does not determine clinical, legal, or safety-critical protocols.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
- Pure Python domain logic with immutable result objects.
- Validates groups, outcomes, duration, and allocation ratio.
- Makes randomization and human review explicit.
- No recruitment, assignment, treatment, or external side effects.

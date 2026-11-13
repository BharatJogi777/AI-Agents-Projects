# Image understanding assistant

## Purpose
Create a structured, evidence-limited review record from image observations supplied by a user or a separate vision adapter.

## Scope
No image loading, vision model, or external API is included. The package preserves visible observations and uncertainty without inventing hidden context.

## Run
Python 3.10+.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Safety
Do not infer identities or sensitive attributes. Distinguish visible text from interpretation, retain uncertainty, and require human review for consequential decisions.

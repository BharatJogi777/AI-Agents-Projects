# Literature review assistant

## Purpose
Organize supplied study metadata into a traceable literature-review outline. It groups studies by theme, preserves reported limitations, and flags duplicate DOI identifiers. It does not retrieve papers or synthesize findings that were not supplied.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
- Pure Python domain logic with immutable result objects.
- Validates required study metadata.
- Deduplicates by DOI when available, otherwise by study ID.
- No network access or external side effects; human review remains necessary.

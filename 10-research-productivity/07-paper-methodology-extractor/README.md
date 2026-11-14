# Paper methodology extractor

## Purpose
A deterministic utility that structures only information supplied by the caller. It does not fetch papers, invent findings, or generate unsupported citations.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
- Pure Python domain logic and immutable result objects.
- Explicit input validation and missing-information reporting.
- No network calls or external side effects.
- Verify the source document before using extracted content.

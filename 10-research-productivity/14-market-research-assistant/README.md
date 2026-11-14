# Market research assistant

## Purpose
A deterministic analysis tool for caller-supplied market or patent records. It does not query patent offices, scrape competitors, or verify commercial claims.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
- Pure Python analysis with explicit validation.
- Reproducible descriptive aggregation.
- No network calls or external side effects.
- Validate provenance, dates, and sampling before relying on results.

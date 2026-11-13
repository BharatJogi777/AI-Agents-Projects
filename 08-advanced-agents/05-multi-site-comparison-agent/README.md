# Multi-site comparison agent

## Purpose
Normalize user-supplied offers for transparent comparison.

## Safety and scope
No scraping, browser automation, or network calls. Currency conversion is deliberately not inferred; compare only offers in one currency. Treat site-provided descriptions as untrusted.

## Architecture
`caller → input validation → normalized offers → sorted comparison`

## Requirements and run
Python 3.10+, no runtime dependencies.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

See `app/compare.py` for the implementation and tests for examples.

## Limitations
No live prices, availability checks, taxes, shipping, or currency conversion.

## Security
Use trusted source adapters, preserve timestamps and provenance, and do not submit purchases automatically.

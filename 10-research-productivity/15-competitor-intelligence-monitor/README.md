# Competitor intelligence monitor

## Purpose
Compare two caller-provided competitor snapshots and identify changed fields. This component does not scrape websites, collect personal data, or infer intent from changes.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
- Deterministic snapshot comparison.
- Stable entity identifiers and explicit field-level changes.
- No network calls, scheduled jobs, or external side effects.
- Record snapshot dates and source URLs in the calling system for auditability.

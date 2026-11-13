# Scheduled Report Generation Agent

Evaluate explicit UTC report schedules and produce due-run decisions with idempotency keys; leave generation and delivery to an authorized worker.

## Safety boundary
This deterministic reference implementation validates supplied data and prepares a reviewable result. It does not autonomously contact external services or execute consequential actions.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

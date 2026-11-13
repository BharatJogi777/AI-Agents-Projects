# Background Task Progress Reporter

Aggregate task progress from validated milestones and expose stalled or failed work with explicit progress semantics.

## Safety boundary
This deterministic reference module validates and reports workflow state. It does not execute external actions or interact with websites.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

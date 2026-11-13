# Long Running Research Agent

Represent a multi-step research run as resumable, checkpointed tasks with explicit evidence references and completion criteria.

## Safety boundary
This deterministic module analyzes supplied records only. It does not perform external actions or change source-system state.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

# Long Running Workflow Monitor

Evaluate workflow execution snapshots for stalled steps, timeout conditions, and state regressions without controlling the workflow engine.

## Safety boundary
This deterministic module analyzes supplied records only. It does not perform external actions or change source-system state.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

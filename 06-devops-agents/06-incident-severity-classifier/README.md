# Incident severity classifier

Classify incident severity from explicit impact, scope, and duration signals with an explainable scoring rubric.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Safety boundary

This is a read-only diagnostic/recommendation tool. It does not connect to clusters, restart workloads, change configuration, or execute runbook steps. Use sanitized snapshots and obtain human approval for operational actions.

## Limitations

The implementation uses deterministic local rules and does not call an LLM or Kubernetes API. Confirm findings against live telemetry and the applicable runbook before taking action.

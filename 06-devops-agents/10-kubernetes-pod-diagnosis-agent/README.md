# Kubernetes pod diagnosis agent

Diagnose common pod and container states from sanitized Kubernetes status snapshots.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Safety and limitations

Read-only local analysis. No Kubernetes API calls, shell commands, restarts, or mutations. Findings are heuristics; verify with pod events, logs, probes, and cluster telemetry before remediation.

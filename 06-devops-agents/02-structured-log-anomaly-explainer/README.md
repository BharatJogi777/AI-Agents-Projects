# Structured log anomaly explainer

Summarize structured JSON logs and flag unusual error-rate or severity changes against an explicit baseline.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Safety boundary

This project is read-only. It does not connect to production systems, execute queries or commands, change infrastructure, restart services, or page responders. Supply sanitized data exports and review recommendations before acting.

## Limitations

Deterministic local reference implementation; no LLM or vendor-specific integration is included. Add authentication, tenant isolation, audit logging, retention controls, and human approval before production integration.

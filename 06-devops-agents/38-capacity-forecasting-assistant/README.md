# Capacity forecasting assistant

Estimate resource exhaustion dates from recent utilization samples and configurable capacity thresholds.

## Safety boundary

This project analyzes supplied operational data and produces recommendations only. It does not connect to production systems, change SLOs, scale infrastructure, or deploy releases.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Outputs depend on the quality of supplied metrics and thresholds. Validate assumptions against service ownership, historical traffic, and production runbooks before acting.

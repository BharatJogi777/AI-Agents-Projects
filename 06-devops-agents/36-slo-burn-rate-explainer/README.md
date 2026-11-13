# SLO burn-rate explainer

Calculate error-budget burn rates over multiple windows and explain fast or sustained budget consumption.

## Safety boundary

This project analyzes supplied operational data and produces recommendations only. It does not connect to production systems, change SLOs, scale infrastructure, or deploy releases.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
```

## Limitations

Outputs depend on the quality of supplied metrics and thresholds. Validate assumptions against service ownership, historical traffic, and production runbooks before acting.

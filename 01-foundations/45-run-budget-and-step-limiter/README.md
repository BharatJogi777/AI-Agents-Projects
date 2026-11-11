# AG-045 — Run budget and step limiter

Independent limits for steps, elapsed wall time, and application-estimated cost, with typed stop reasons.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

Cost values are estimates supplied by the caller, not billing guarantees. Enforce provider quotas separately.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

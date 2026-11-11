# AG-023 — Model fallback router

Routes text-generation requests through compatible models/providers, filters by declared capabilities, checks health, and falls back after exceptions or empty responses.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This is sequential fallback, not a cost/latency optimizer. Production systems should classify retryable errors, add per-provider deadlines, emit sanitized telemetry, and avoid hiding authorization/configuration failures. Tests are authored but not yet executed.

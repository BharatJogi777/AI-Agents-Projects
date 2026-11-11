# AG-050 — FastAPI agent endpoint

A FastAPI adapter with strict Pydantic input validation, bounded prompts, health endpoint, and sanitized internal errors.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

This sample omits authentication, rate limiting, persistence, quotas, and background execution. Add those before public deployment.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

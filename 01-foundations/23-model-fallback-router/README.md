# AG-023 — Model fallback router

Routes a text request through provider/model pairs compatible with declared capabilities. It honors provider preference, optional health checks, and sequential fallback, returning the successful model and attempted route identifiers.

## Architecture
- `model_router/router.py`: provider protocol, route result, compatibility filtering, health checks, and fallback loop.
- `registry.py`: capability registry dependency from AG-022.
- `app.py`: public router facade.

## Execution flow
1. Reject an empty prompt.
2. Select models meeting required tool/JSON/context constraints.
3. Order providers by caller preference, then stable provider name.
4. Skip missing/unhealthy providers.
5. Attempt chat sequentially; accept only non-empty text and otherwise continue.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This is not cost/latency optimization. Broad provider failures are intentionally not exposed to callers; production use should add typed retry classification, per-provider deadlines, circuit breakers, and sanitized telemetry. Tests are authored; local execution remains pending.

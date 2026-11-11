# AG-018 — Circuit-breaker model client

A thread-safe circuit breaker protects model/provider calls. It transitions CLOSED → OPEN after a configurable failure threshold, waits for a recovery interval, allows exactly one HALF_OPEN probe, and closes on success or reopens on failure.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The breaker is process-local. In multi-worker deployments each process has its own state unless a shared coordination store is added. Tune thresholds from observed provider behavior and combine with timeouts, retries, and request-level budgets. Local test execution is pending.

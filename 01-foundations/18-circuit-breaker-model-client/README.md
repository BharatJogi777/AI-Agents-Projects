# AG-018 — Circuit-breaker model client

A thread-safe CLOSED/OPEN/HALF_OPEN circuit breaker that rejects calls during provider outages and permits only one recovery probe after the cool-down interval.

## Architecture
- `circuit_breaker/contracts.py`: states, snapshots, public exception, and internal call permit.
- `circuit_breaker/breaker.py`: locked state transitions, recovery timing, and generation-aware completion handling.
- `app.py`: compatibility facade.

## Execution flow
1. A call acquires a permit while CLOSED, or is rejected while OPEN.
2. After the recovery interval, exactly one caller obtains the HALF_OPEN probe permit.
3. Success closes the circuit and resets failures; probe failure reopens it.
4. A generation number prevents late completions from older in-flight calls from incorrectly closing a newer OPEN circuit.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This implementation counts failures, not rolling failure rates. Production systems may need rolling windows, metrics, bulkheads, per-model keys, and distributed coordination. The breaker is process-local. Local test execution remains pending.

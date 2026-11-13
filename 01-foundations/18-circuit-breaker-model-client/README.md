# AG-018 — Circuit-breaker model client

A thread-safe, process-local circuit breaker that protects an LLM/model provider from repeated calls during an outage.

## Why it exists

Retries handle short-lived transient errors. But if an Ollama/OpenAI-compatible provider is unhealthy, repeatedly retrying every request adds load and increases latency. A circuit breaker temporarily rejects calls, gives the dependency time to recover, and allows a controlled probe.

## State machine

- **CLOSED:** requests are allowed. Consecutive ordinary operation failures are counted.
- **OPEN:** requests are rejected immediately with `CircuitOpen`.
- **HALF_OPEN:** after the recovery interval, one caller is allowed to probe the dependency. Other callers are rejected until that probe completes.

A successful call closes the circuit and resets the failure count. A failed half-open probe opens it again and starts a new recovery interval.

```text
CLOSED -- failure threshold reached --> OPEN
OPEN -- recovery interval elapsed --> HALF_OPEN
HALF_OPEN -- probe succeeds --> CLOSED
HALF_OPEN -- probe fails --> OPEN
```

## Usage

```python
from circuit_breaker import CircuitBreaker, CircuitOpen

breaker = CircuitBreaker(failure_threshold=3, recovery_seconds=15)

try:
    response = breaker.call(model_client.generate, prompt="Summarize this log")
except CircuitOpen:
    # Return a controlled fallback or ask the caller to retry later.
    response = cached_response
```

Use a separate breaker per provider/model endpoint (and often per deployment/region). Do not share one breaker across unrelated dependencies.

## Design and safety

- State transitions and snapshots are protected by a thread lock.
- The protected operation runs outside the lock; slow provider I/O does not block other state reads.
- Generation tokens stop late completions from old in-flight calls mutating a newer circuit state.
- Only ordinary `Exception` failures count. Cancellation, KeyboardInterrupt, and SystemExit propagate without being recorded as dependency failures. A cancelled half-open probe releases its probe slot.
- The clock is injectable and uses monotonic time by default.
- The breaker is in-memory and process-local. Multiple workers/pods have independent state; distributed coordination is intentionally not included.
- This is a consecutive-failure threshold, not a rolling error-rate window. Add metrics, alerting, bulkheads, request timeouts, and fallback policy around it in a production service.
- Prefer `call()`. The manual `before_call()/record_*` methods exist for compatibility and cannot provide the same per-call generation safety under concurrent use.

## Layout

- `circuit_breaker/contracts.py`: state enum, snapshot, and public exception.
- `circuit_breaker/breaker.py`: thread-safe state machine and call wrapper.
- `tests/test_breaker.py`: deterministic state, concurrency, late-completion, and cancellation tests.
- `app.py`: compatibility facade.

## Run locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Tests need no model server or network access. They are authored in the repository; run them locally to verify in your environment.

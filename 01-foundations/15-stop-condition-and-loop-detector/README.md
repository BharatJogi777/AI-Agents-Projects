# AG-015 — Stop-condition and loop detector

A deterministic termination policy for agent controllers. It fingerprints JSON-compatible state with canonical serialization, detects repeated states in bounded rolling history, and applies a stable priority to cancellation, deadlines, final answers, step budgets, and repetition.

## Architecture

- `stop_policy/fingerprint.py`: stable SHA-256 state fingerprints with finite-JSON and byte-size validation.
- `stop_policy/detector.py`: thread-safe bounded rolling history and repeat detection.
- `stop_policy/policy.py`: centralized stop-priority policy.
- `app.py`: compatibility facade, including the original static fingerprint method.

## Execution flow

1. Construct a state snapshot containing relevant tool names, arguments, and state versions (never credentials).
2. Canonically serialize and hash the snapshot.
3. Compare the fingerprint against recent bounded history.
4. Pass the detector decision and controller signals to `evaluate_stop()`.
5. Apply priority: cancellation → deadline → final answer → step limit → repeated state.

## Run and test

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Repeated-state detection is a heuristic, not proof of an infinite loop. Include all state that changes the meaning of an action. Tests are authored; local execution remains pending.

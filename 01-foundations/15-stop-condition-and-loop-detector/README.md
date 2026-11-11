# AG-015 — Stop-condition and loop detector

Agent loops need explicit termination rules beyond “the model said it is done.” This module fingerprints normalized states, detects repeated tool/state cycles within a bounded rolling window, and centralizes deterministic stop priority: cancellation, deadline, final answer, step budget, then repetition.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

A repeated state is a heuristic signal, not proof of a logical infinite loop. Choose fingerprints that include relevant tool arguments and state versions; avoid placing secrets in state snapshots. Local test execution is pending.

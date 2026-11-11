# AG-014 — Bounded agent loop

A framework-independent controller around an injected single-iteration callback. It enforces independent step, total tool-call, and consecutive-error budgets and returns a report for successful completion or repeated failures.

## Architecture

- `agent_loop/contracts.py`: immutable configuration, step result, report, and budget exceptions.
- `agent_loop/runner.py`: deterministic budget accounting and stop handling.
- `app.py`: backward-compatible public exports.

## Execution flow

1. The caller supplies a callback that performs one bounded model interaction.
2. The controller validates its result and rejects negative/non-integer counters.
3. Tool-call counts are checked before they can exceed the configured budget.
4. Consecutive errors accumulate and reset after a clean step.
5. A final answer or error threshold returns a report; exceeding step/tool budgets raises a typed exception.

## Run and test

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This loop budget does not replace per-tool deadlines, a request-wide deadline, cancellation, or provider rate limits. Tests are authored; local execution remains pending.

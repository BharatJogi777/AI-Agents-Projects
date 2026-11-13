# Self-reflection loop with limits

Run a task, evaluate its result, and retry with feedback while enforcing explicit attempt and stop conditions.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Structure
- `app/reflection.py`: deterministic orchestration component with injected model/worker boundaries.
- `tests/test_reflection.py`: success and failure-path tests.

The core does not assume model output is trustworthy. Validate proposals before side effects, bound retries and routing, record audit events without secrets, and require human approval for consequential operations. These local examples are not distributed schedulers.

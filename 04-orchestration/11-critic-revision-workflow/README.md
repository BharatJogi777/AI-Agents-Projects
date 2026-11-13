# Critic-revision workflow

Iteratively critique and revise an artifact under a strict iteration budget, retaining review history.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Structure
- `app/critic.py`: deterministic orchestration component with injected model/worker boundaries.
- `tests/test_critic.py`: success and failure-path tests.

The core does not assume model output is trustworthy. Validate proposals before side effects, bound retries and routing, record audit events without secrets, and require human approval for consequential operations. These local examples are not distributed schedulers.

# Intent-based specialist router

Map normalized intent labels to specialist handlers and reject unknown or ambiguous routing decisions.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Structure
- `app/intent_router.py`: deterministic orchestration component with injected model/worker boundaries.
- `tests/test_intent_router.py`: success and failure-path tests.

The core does not assume model output is trustworthy. Validate proposals before side effects, bound retries and routing, record audit events without secrets, and require human approval for consequential operations. These local examples are not distributed schedulers.

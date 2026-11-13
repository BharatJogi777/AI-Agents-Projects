# Tool router graph

Route validated typed tool requests through an allowlisted graph with bounded transitions and explicit result state.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Structure
- `app/tool_graph.py`: deterministic orchestration component with injected model/worker boundaries.
- `tests/test_tool_graph.py`: success and failure-path tests.

The core does not assume model output is trustworthy. Validate proposals before side effects, bound retries and routing, record audit events without secrets, and require human approval for consequential operations. These local examples are not distributed schedulers.

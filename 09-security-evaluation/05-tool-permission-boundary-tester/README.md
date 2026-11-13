# Tool permission boundary tester

A deterministic default-deny evaluator for agent tool requests against explicit principal/tool grants.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

This evaluates a supplied policy snapshot only; enforce authorization again at the actual tool server.
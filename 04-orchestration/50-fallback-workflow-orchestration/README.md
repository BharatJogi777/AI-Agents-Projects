# Fallback Workflow Orchestration

AG-200 executes ordered workflow alternatives until one succeeds and retains a structured attempt history.

## Features

- Ordered fallback strategies with unique names
- Captures failure details and returns the first successful result
- Explicit failure when all strategies fail

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The runtime uses only the Python standard library. This is an in-process reference component; production systems should add durable attempt storage, telemetry, timeouts, and cancellation.

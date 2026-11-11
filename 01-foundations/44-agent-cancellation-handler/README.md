# AG-044 — Agent cancellation handler

A cooperative cancellation token that carries a bounded reason and raises at explicit checkpoints.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

Cancellation cannot forcibly stop blocking code. Pass the token through every long-running boundary and clean up resources in finally blocks.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

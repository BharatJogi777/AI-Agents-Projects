# AG-041 — Agent state machine

A finite-state machine that validates legal transitions and prevents mutation after terminal states.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

The model may suggest a transition, but application code owns this state machine. Add durable persistence and versioned transitions before using it across workers.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

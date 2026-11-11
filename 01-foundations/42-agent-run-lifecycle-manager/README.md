# AG-042 — Agent run lifecycle manager

An in-memory, thread-safe registry for isolated runs with UTC timestamps and guarded lifecycle changes.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

This registry is process-local. Use a database transaction and optimistic locking for multi-process deployments.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

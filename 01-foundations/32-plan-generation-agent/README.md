# AG-032 — Plan generation agent

Generate a typed execution plan through an injected planner, enforcing task limits and a stable JSON contract.

## Run and test

Requires Python 3.12+.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
```

## Design and limitations

Model behavior is injected behind a small interface; deterministic code validates invariants before state changes. Tests do not require a model or network. This is a focused learning implementation, not a complete production platform. In-memory data is process-local; add durable storage, authentication, encryption, retention, observability, and operational controls before multi-user deployment. Treat model output as untrusted. Tests are authored; local execution remains pending.

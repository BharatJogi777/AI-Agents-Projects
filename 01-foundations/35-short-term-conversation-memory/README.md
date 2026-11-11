# AG-035 — Short-term conversation memory

Maintain a bounded chronological message window while preserving system instructions and complete turns.

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

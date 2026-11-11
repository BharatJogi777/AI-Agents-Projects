# AG-011 — Typed tool registry

A startup-time allowlist that binds a stable tool name to a Pydantic argument model and a trusted Python handler. The registry exports provider function schemas, rejects duplicate/invalid names, validates every call again at execution time, and hides handler exception text from the model.

## Architecture

- `tool_registry/registry.py`: registration, schema export, strict validation, and dispatch.
- `tool_registry/errors.py`: distinct configuration-time and invocation-time failures.
- `app.py`: compatibility facade for the first tutorial revision. New imports should use `tool_registry`.

## Execution flow

1. Application startup registers trusted handlers and their input models.
2. The provider receives `provider_schemas()`; those schemas help the model form a call but are not a security boundary.
3. The returned tool name is resolved against the local allowlist.
4. Arguments are revalidated with Pydantic strict mode.
5. Only the registered handler is invoked. Handler failures are wrapped without leaking exception messages.

## Run and test

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

No model or network is required. The registry is not a sandbox: handlers still need authorization, deadlines, resource limits, and safe side-effect design. Tests are authored; local execution remains pending.

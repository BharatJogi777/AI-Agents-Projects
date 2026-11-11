# AG-026 — Function-call parser

Normalizes provider tool/function call payloads before any handler is invoked. It validates the call envelope, call ID, function-name syntax, allowlist membership, JSON object arguments, and byte-size limits.

## Architecture
- `function_calls/contracts.py`: normalized immutable call record and parser exception.
- `function_calls/parser.py`: envelope parsing, JSON validation, allowlist checks, and handler dispatch.
- `app.py`: compatibility facade.

## Execution flow
Parse the provider call against the server-owned allowlist. Arguments supplied as JSON text are parsed; dictionary arguments are independently serialized with non-finite numbers disabled and checked against the same byte limit. Dispatch resolves a trusted local handler and wraps its exception without exposing internals.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Parsing is not schema validation or authorization. Validate arguments against the tool's actual schema and authorize the caller before side effects. Tests are authored; local execution remains pending.

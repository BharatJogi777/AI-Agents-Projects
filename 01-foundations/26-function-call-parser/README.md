# AG-026 — Function-call parser

Normalizes function/tool-call payloads from LLM providers into a typed record. It validates call IDs, function names, allowlists, JSON arguments, object shape, and argument-size bounds before application dispatch.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Parsing is not authorization: validate arguments against the actual tool schema, authorize the caller, and apply side-effect/idempotency controls before invoking handlers. Tests are authored but not yet executed.

# AG-012 — Tool argument validation agent

A defensive boundary for model-generated tool calls. Tool-call JSON is treated as untrusted input, bounded before parsing, validated against an allowlisted Pydantic model, and only then passed to a trusted handler.

## Architecture

- `tool_gate/gate.py`: allowlist lookup, JSON parsing, byte limits, strict schema validation, bounded field feedback, and handler dispatch.
- `tool_gate/errors.py`: separates rejected model input from trusted-handler failures.
- `app.py`: demo `SearchArgs` and backward-compatible exports.

## Execution flow

1. Reject unknown tool names before touching arguments.
2. Parse a JSON string only after enforcing the encoded byte limit.
3. Require an object containing JSON-compatible values; reject NaN/Infinity.
4. Validate with Pydantic strict mode (extra-field behavior comes from the model's config).
5. Invoke the handler and return a stable success envelope. Do not send internal handler exceptions to the model.

## Run and test

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The sample search handler is deterministic and performs no network access. Add authorization and tenant scoping before exposing real tools. Tests are authored; local execution remains pending.

# AG-012 — Tool argument validation agent

A defensive boundary for model-generated tool calls. Tool-call JSON is treated as untrusted input, bounded before parsing, validated against an allowlisted Pydantic model, and only then passed to a trusted handler.

## Architecture

- `tool_gate/gate.py`: allowlist lookup, JSON parsing, duplicate-key rejection, byte limits, strict schema validation, bounded field feedback, handler dispatch, and result normalization.
- `tool_gate/errors.py`: separates rejected model input from trusted-handler failures.
- `tool_gate/__init__.py`: public API including configurable `GateLimits`.
- `app.py`: demo `SearchArgs` and backward-compatible exports.
- `tests/test_gate.py`: malformed JSON, duplicate keys, coercion, unknown tools, size limits, output safety, and error-boundary tests.

## Execution flow

1. Reject unknown tool names before parsing their arguments.
2. For string arguments, enforce the UTF-8 byte limit before JSON parsing.
3. Reject duplicate object keys and non-standard JSON constants such as NaN and Infinity.
4. Require an object containing JSON-compatible values.
5. Validate with Pydantic strict mode. Use `extra="forbid"` on argument models to reject unexpected fields.
6. Invoke the trusted handler only after validation.
7. Require handler output to be finite JSON and within the configured result byte limit. Return a detached JSON-compatible value.

## Run and test

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The sample search handler is deterministic and performs no network access. Tests are authored; local execution remains pending.

## Production boundaries

Validation does not equal authorization. Add user/tenant authorization before invoking real tools. Side-effecting handlers need idempotency and audit controls. Run untrusted or high-risk tools in isolated workers with deadlines, cancellation, concurrency limits, and restricted network/filesystem access. Never expose exception messages or stack traces to the model.

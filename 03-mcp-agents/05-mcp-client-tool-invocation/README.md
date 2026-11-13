# AG-105 — MCP client tool invocation

A policy-enforcing invocation layer around an MCP `ClientSession`. It checks the tool allowlist, validates that arguments are a JSON object, applies a deadline, and emits an audit event for success or failure.

## Setup

Python 3.11+, MCP SDK 1.x, Pydantic 2.

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Example

```python
from app.services.invoker import ToolInvoker

invoker = ToolInvoker(
    session=mcp_session,
    allowed_tools={"lookup_order"},
    timeout_seconds=8,
    audit=lambda event: print(event),
)
result = await invoker.invoke("lookup_order", {"order_id": "ORD-1001"})
```

The session must already be initialized and connected by its transport owner. The invoker does not create a transport or silently retry side effects.

## Controls

- Deny-by-default allowlist.
- Object-only JSON arguments; reject unknown tools before network I/O.
- Per-call timeout and typed errors.
- Audit event records tool name, outcome, elapsed time, and correlation ID; it deliberately excludes arguments and result payloads.
- MCP tool results are returned to the caller as untrusted data.

## Limitations

This wrapper does not validate arguments against the server's full JSON Schema; use discovered schemas for a separate validation layer. The caller owns session lifecycle, authentication, transport security, and result interpretation.

# AG-111 — Multi-server MCP client

Manage several initialized MCP sessions behind one namespaced client. Discover tools from each server, expose names such as `orders.lookup`, and route invocations to the correct session. The manager accepts sessions created by stdio or Streamable HTTP transports; transport setup and teardown remain the caller's responsibility.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Example

```python
manager = MultiServerClient()
manager.add_server("orders", orders_session, allowed_tools={"lookup"})
manager.add_server("inventory", inventory_session, allowed_tools={"check_stock"})
tools = await manager.discover()
result = await manager.call("orders.lookup", {"order_id": "ORD-42"})
```

## Safety

- Every server namespace and tool permission is explicit.
- Tool names are namespaced to avoid collisions.
- Discovery results are filtered through per-server allowlists.
- A server cannot be registered twice under the same namespace.
- Sessions are injected; the manager never launches arbitrary subprocesses or accepts arbitrary URLs.
- The caller must close all transport/session context managers.

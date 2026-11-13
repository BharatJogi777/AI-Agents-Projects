# AG-112 — MCP server connection pool

A transport-neutral asynchronous pool for connected MCP client sessions. It bounds concurrent sessions, reuses idle sessions, waits for leases to return, and closes all sessions during shutdown.

## Architecture

- The caller supplies an async session factory and close callback. This keeps stdio and Streamable HTTP transport setup outside the pool.
- `SessionPool.acquire()` is an async context manager. A session is exclusively leased until the context exits.
- `max_size` bounds created sessions; `acquire_timeout` bounds waiting for capacity.
- Shutdown rejects new leases, waits for active leases and in-flight connection creation, then closes sessions.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Integration

Create a factory that connects using the official MCP Python SDK and returns a started `ClientSession`. The pool deliberately does not hide transport lifecycle or own SDK context managers; adapt those into the supplied factory/closer in the application layer.

## Operational notes

Use one pool per upstream identity and authorization context. Do not share a session across principals. Set capacity from upstream limits and observe lease wait time, pool saturation, connection failures, and shutdown duration. A production adapter should invalidate sessions after transport/protocol failures rather than returning broken sessions to the pool.

## Limitations

This learning implementation does not perform health checks, idle eviction, or automatic broken-session detection. Tests are authored; run them in your environment before deployment.

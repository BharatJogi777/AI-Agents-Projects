# AG-108 — MCP server health inspector

Perform a protocol-level health check against an already connected MCP client session. A successful TCP connection alone is not sufficient: this inspector verifies that the MCP session can respond to ping and return its server identity.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Integration

Create and initialize an MCP `ClientSession` using your chosen transport, then call:

```python
from app.health import inspect_session

report = await inspect_session(session, timeout_seconds=3)
print(report)
```

The transport owner remains responsible for opening and closing the session.

## Health semantics

- `healthy`: protocol ping succeeded and server identity was received.
- `unhealthy`: timeout or protocol/connection error.
- The report includes duration and a safe error category, not raw exception details or credentials.
- This check does not prove that every tool's backing dependencies are healthy.

# AG-128 — GitHub pull-request MCP assistant

A read-only typed GitHub pull-request reader suitable for wrapping as an MCP tool. It validates repository coordinates, uses an injected HTTP transport, and returns a small typed context object.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Use a fine-grained token with minimum repository read permissions. Never expose merge, approve, comment, or push actions through this reader. Add transport timeouts, rate-limit handling, pagination for changed files, and audit events in the MCP adapter.

## Limitations
This project retrieves pull-request metadata only; it does not perform code review or modify GitHub state.

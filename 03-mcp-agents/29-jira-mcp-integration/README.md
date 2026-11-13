# AG-129 — Jira MCP integration

A read-only Jira issue lookup core that maps API payloads to a stable typed model.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Configure a Jira Cloud HTTPS base URL and a dedicated service identity with least-privilege browse access. Store API credentials in a secret manager; use proper HTTP Basic authentication encoding in the transport adapter, set connect/read timeouts, and redact authorization headers. Expose issue lookup only after caller authorization.

## Limitations
This is an injected-transport client core, not a complete MCP server. It intentionally has no create, update, transition, or comment operation.

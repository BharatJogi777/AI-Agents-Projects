# AG-127 — GitHub issue MCP integration

A typed GitHub Issues API boundary designed to be wrapped by MCP tools. HTTP transport is injected so core logic can be tested without network access.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Store tokens in a secret manager and grant minimum repository permissions. Never log the token. Add pagination, retry-after handling, rate-limit awareness, request timeouts, and organization policy checks in the HTTP adapter. Pull requests are excluded from issue results.

## Limitations
This package is an API client core, not a running MCP server. Provide an authenticated HTTP client and register narrowly scoped read tools.

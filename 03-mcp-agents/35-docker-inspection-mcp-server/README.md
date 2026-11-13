# Docker inspection MCP server

A read-only MCP integration that exposes a narrowly scoped operational capability.

## Features
- Typed, bounded queries with input validation.
- Read-only API surface; no mutation tools are registered.
- Unit tests isolate the business logic from external infrastructure.
- Secrets and credentials are read from environment/provider configuration, never hard-coded.

## Requirements
Python 3.11+. Install with `pip install -e ".[dev]"`.

## Run
Configure the relevant provider credentials and access first, then run:
```bash
python -m app.server
```

## Security
Use a dedicated least-privilege identity and restrict network egress. Treat returned infrastructure metadata as sensitive. Do not expose this server to untrusted clients without authentication at the transport boundary. Set provider-side read-only permissions; application-level read-only tools are not a substitute.

## Tests
```bash
pytest -q
```

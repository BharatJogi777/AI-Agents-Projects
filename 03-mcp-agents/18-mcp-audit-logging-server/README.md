# AG-118 — MCP audit logging server

A transport-independent JSON Lines audit sink for MCP middleware.

- UTC timestamp on each event.
- Strict allowlist: arbitrary arguments, credentials, and payloads are discarded.
- Thread-safe append and owner-only permissions on newly created files.
- Validates metadata types and non-negative duration.

## Run
```bash
pip install -e '.[dev]'
pytest
```

## Integration
Record request ID, authenticated principal, tool name, allow/deny decision, duration, and status. Keep audit records separate from application logs and ship them to protected centralized storage with retention and integrity controls.

## Limitations
Local files are not tamper-proof or multi-process transactional. Use a durable centralized audit service for high-assurance systems. Tests are authored, not executed here.

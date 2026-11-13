# AG-124 — PostgreSQL read-only MCP server

Provides a conservative single-statement SQL gate for a read-only database tool.

## Run
```bash
pip install -e '.[dev]'
pytest
```

**Important:** SQL text inspection is not a security boundary. Connect with a dedicated PostgreSQL role that has SELECT-only grants, enforce statement and row limits, set transaction read-only, use query timeouts, and allowlist schemas/tables. Parameterize all values; never concatenate user input.

## Limitations
The validator is intentionally restrictive and not a SQL parser. Production authorization must be enforced by database privileges and a trusted query layer.

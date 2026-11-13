# AG-125 — Redis diagnostics MCP server

Sanitizes Redis INFO output to a small operational allowlist and calculates cache hit rate.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Use a read-only Redis ACL user and expose only approved INFO sections. Do not expose CONFIG, KEYS, FLUSH*, MONITOR, or arbitrary command execution to an agent. Treat hostnames, keyspace names, and metrics as potentially sensitive.

## Limitations
This package only transforms INFO data; it does not open a Redis connection. Add a bounded Redis client adapter and authentication outside this module.

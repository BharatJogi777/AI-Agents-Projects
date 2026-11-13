# AG-119 — MCP rate-limited tool server

A thread-safe token bucket for MCP tool middleware.

- Independent buckets keyed by authenticated principal and canonical tool.
- Configurable burst capacity and refill rate.
- Supports weighted request costs and injected monotonic clock.

## Run
```bash
pip install -e '.[dev]'
pytest
```

Build keys from verified identity and tool name; authenticate and authorize before consuming quota. Expose rejection metrics without leaking identities.

## Limitations
State is process-local. Multiple replicas need shared atomic storage such as Redis, plus inactive-key cleanup and tenant/global quotas.

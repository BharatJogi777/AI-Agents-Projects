# AG-036 — Session-scoped memory store

Provides a thread-safe, process-local key/value store with session isolation, TTL expiry, injected monotonic clock, and a global bounded capacity. Reads update LRU order; expired entries are purged before writes and size reporting.

## Modules
- `session_memory/contracts.py`: immutable entry metadata.
- `session_memory/store.py`: TTL/LRU operations, capacity enforcement, and session deletion.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Memory is not shared across processes and is lost on restart. Use a durable shared store for production; add authentication, encryption, per-tenant quotas, and retention controls. Local test execution remains pending.
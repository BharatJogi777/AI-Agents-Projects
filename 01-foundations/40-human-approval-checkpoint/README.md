# AG-040 — Human approval checkpoint

Creates expiring, one-time approval requests bound to a SHA-256 hash of canonical JSON action data. Decisions reject changed payloads, use constant-time digest comparison, and are protected against concurrent double decisions with a lock.

## Modules
- `approval_gate/contracts.py`: approval record and not-found error.
- `approval_gate/gate.py`: canonical payload hashing, request lifecycle, expiry, and atomic decision.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This protects payload integrity within one process; it does not authenticate approvers or authorize access to an approval ID. Production needs authenticated identities, RBAC, durable transactional one-time decisions, audit logs, and a secure delivery channel. Local test execution remains pending.
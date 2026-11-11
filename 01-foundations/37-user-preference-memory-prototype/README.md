# AG-037 — User preference memory prototype

Stores only explicit, user-confirmed preferences from a small non-sensitive category allowlist. Records include UTC provenance timestamps and can be deleted by category or user.

## Modules
- `preference_memory/contracts.py`: immutable preference record.
- `preference_memory/store.py`: consent gate, category allowlist, user isolation, provenance, and deletion.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

No inference or automatic capture is implemented. This is an in-memory prototype, not a consent-management or compliance platform. Production storage needs access controls, encryption, audit logs, retention, and verified deletion. Local test execution remains pending.
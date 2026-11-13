# Persistent workflow state store

Store versioned JSON workflow snapshots in SQLite with safe parameterized queries and optimistic concurrency.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Operational considerations
SQLite is suitable for a local single-host demonstration. Production multi-worker deployments should use a shared transactional database, schema migrations, encryption/access controls, retention policies, and observable conflict handling. Never persist credentials or raw secrets in workflow state.

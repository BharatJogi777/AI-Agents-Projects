# Workflow resume after restart

Persist workflow progress after each successful step and resume only the unfinished steps after process restart.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Operational considerations
SQLite is suitable for a local single-host demonstration. Production multi-worker deployments should use a shared transactional database, schema migrations, encryption/access controls, retention policies, and observable conflict handling. Never persist credentials or raw secrets in workflow state.

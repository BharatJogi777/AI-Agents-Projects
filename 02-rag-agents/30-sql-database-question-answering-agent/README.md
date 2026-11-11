# AG-80 — SQL database question-answering agent

Execute bounded read-only SQLite SELECT queries with table allowlists, an authorizer, execution budget, and row limits.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Safety and limitations

This is a constrained SQLite execution component, not a natural-language-to-SQL model. The caller must independently validate query intent and supply an explicit table allowlist. Use a dedicated read-only database connection and least-privilege credentials in deployed systems.

Tests are authored but have not been run locally.

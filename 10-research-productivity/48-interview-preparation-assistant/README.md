# AG-498: Interactive study coach

Build a role-specific interview practice plan from supplied competencies, experience examples, and target interview date.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This deterministic reference implementation uses only caller-supplied data. It does not connect to external learning platforms or claim that generated plans guarantee outcomes. Tests are authored but have not been executed in this repository workflow.

# Flaky Test Investigator

Analyzes repeated test outcomes and execution durations to identify likely flaky tests. It reports pass/fail transitions, failure rates, and duration spread without claiming a root cause.

## Run
```bash
pip install -e ".[dev]"
python -m app.flakiness
pytest
```

## Limits
Input records should come from isolated repeated runs with comparable environments. Correlation is not proof of a race or timing defect; inspect logs and reproduce before changing code.

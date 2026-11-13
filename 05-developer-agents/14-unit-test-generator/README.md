# Unit Test Generator

Creates starter pytest test cases from a small, explicit function contract. It covers valid examples, invalid inputs, and boundary cases as supplied by the caller; it does not inspect or execute source code.

## Run
```bash
pip install -e ".[dev]"
python -m app.testgen
pytest
```

## Limitations
Generated tests are templates. They must be adapted to actual behavior, fixtures, side effects, and project conventions. No generated code is written automatically.

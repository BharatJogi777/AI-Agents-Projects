# Property-Based Test Generator

Builds deterministic property-test templates from explicit input domains and invariants. It does not execute generated expressions or import the target module.

## Run
```bash
pip install -e ".[dev]"
python -m app.property_tests
pytest
```

## Safety and limits
Expressions are emitted as source for human review, never evaluated here. Validate generated strategies against the real function contract and add shrinking or Hypothesis integration only after reviewing the domain.

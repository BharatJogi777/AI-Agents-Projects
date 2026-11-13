# Type Error Diagnosis Agent

Classifies common mypy/pyright-style diagnostics into actionable categories: optional values, incompatible assignments, missing attributes, argument mismatch, and unknown rules.

## Run
```bash
pip install -e ".[dev]"
python -m app.type_diagnosis
pytest
```

## Limitations
Message formats are tool/version dependent. The classifier offers hypotheses, not type-checker execution or a definitive fix.

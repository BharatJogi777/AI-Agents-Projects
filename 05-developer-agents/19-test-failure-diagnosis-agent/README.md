# Test Failure Diagnosis Agent

Parses common pytest failure output into structured failure records and conservative diagnostic hints. It preserves traceback excerpts and distinguishes assertion failures, import errors, collection errors, and unexpected exceptions.

## Run
```bash
pip install -e ".[dev]"
python -m app.diagnose
pytest
```

## Limitations
Text matching cannot establish root cause. Keep the original test output, inspect source context, and reproduce in the same environment before accepting a diagnosis.

# Linter Remediation Assistant

Maps common lint rule identifiers to conservative remediation guidance and review checks. It never edits source files or suppresses rules automatically.

## Run
```bash
pip install -e ".[dev]"
python -m app.remediate
pytest
```

## Limits
Rule messages vary by tool and version. Guidance is generic; inspect the exact rule documentation and confirm the proposed change preserves behavior.

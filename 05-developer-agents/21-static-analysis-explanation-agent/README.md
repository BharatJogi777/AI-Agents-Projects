# Static Analysis Explanation Agent

Normalizes static-analysis findings into clear explanations with severity, source location, likely impact, and a verification checklist. It preserves tool-provided evidence and avoids claiming a finding is definitely exploitable.

## Run
```bash
pip install -e ".[dev]"
python -m app.explain
pytest
```

## Limitations
Provide structured findings from a trusted scanner. This project does not run scanners or validate source semantics; humans must confirm reachability and remediation.

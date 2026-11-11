# AG-047 — Untrusted tool-output handling

A bounded JSON envelope labels tool output as untrusted and redacts common credential-like key/value patterns.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

Regex redaction is incomplete. Prefer structured schemas and dedicated secret scanning; never rely on this demo as the only DLP control.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

# AG-046 — Prompt injection awareness demo

A prompt builder labels policy, user request, and retrieved data separately, plus a deterministic allowlist/approval check.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

Delimiters are not a security boundary. Enforce authorization in trusted code, minimize tool privileges, and treat retrieved content as hostile.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

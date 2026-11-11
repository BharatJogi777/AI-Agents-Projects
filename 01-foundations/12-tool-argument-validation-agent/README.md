# AG-012 — Tool argument validation gate

Every model-generated tool call is untrusted input. This gate checks the tool name against an allowlist, parses JSON, enforces a strict Pydantic schema, and only then invokes the trusted handler. Validation errors become bounded field-path feedback; handler failures remain distinct runtime failures.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The included search handler is a deterministic stub and performs no network access. Tests cover malformed JSON, wrong top-level types, strict type validation, extra fields, unknown tools, and handler failures. Local test execution is pending.

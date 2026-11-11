# AG-011 — Typed tool registry

A reusable registry maps stable tool names to trusted Python handlers and strict Pydantic argument models. It exports provider-compatible function schemas, rejects duplicate names and unknown tools, validates every invocation, and wraps handler failures without exposing internal exception details.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

No LLM or network connection is required. A registry is an allowlist, not a sandbox: handlers must still enforce authorization, timeouts, and resource limits. Tests are authored; local execution is pending.

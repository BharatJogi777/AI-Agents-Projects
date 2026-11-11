# AG-028 — Deterministic rule plus LLM router

Applies cheap, explicit deterministic rules before invoking an injected LLM classifier. Rule matches have priority; model output is constrained to a configured route allowlist.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The LLM is not allowed to invent destinations. Add confidence thresholds, abstention, audit logs, and human escalation before using this pattern for high-impact routing. Tests are authored but not yet executed.

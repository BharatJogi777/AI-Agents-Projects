# AG-028 — Deterministic rule plus LLM router

Applies ordered deterministic routing rules first and calls an injected LLM classifier only when no rule matches. Both rule destinations and model-selected destinations are constrained to a server-owned allowlist.

## Architecture
- `rule_router/contracts.py`: normalized route result with confidence and source.
- `rule_router/router.py`: rule evaluation, LLM fallback, and route allowlist enforcement.
- `app.py`: compatibility facade.

## Execution flow
Validate input, evaluate rules in registration order, and immediately return the first match. Only unmatched requests reach the classifier. A model-selected route outside the allowlist is rejected.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

The model is not permitted to invent destinations. Add abstention, audit logging, human escalation, and domain-specific evaluation before high-impact routing. Tests are authored; local execution remains pending.

# Secret leakage scanner for prompts

A deterministic Python security control for agent workflows. These utilities support defense-in-depth; they are not a substitute for secret management, authorization at the tool server, or human risk review.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Avoid storing real credentials in fixtures or logs. Review policy configuration before deployment.
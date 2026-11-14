# AG-485: Project risk register assistant

Validate and rank project risks using supplied likelihood and impact ratings.

## Scope and limitations

This deterministic tool scores only user-provided assessments. It does not discover risks or establish their probability. Review ratings and mitigation plans with project stakeholders.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

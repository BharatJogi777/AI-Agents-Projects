# Hypothesis critique agent

## Purpose
A deterministic research-support component operating on caller-provided inputs. It does not browse external sources or establish factual truth. Review its output before making decisions.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
- Pure Python domain logic with input validation.
- Explicit limitations and human-review boundary.
- No network access, credentials, or external side effects.

# Tool argument fuzz tester

A deterministic, dependency-light security testing component. It does not call an LLM or prove that a production agent is secure.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Review findings before taking action. Keep secrets out of fixtures and logs; enforce security controls at the execution boundary.
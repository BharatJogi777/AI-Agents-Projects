# Developer knowledge-base assistant

Search curated engineering notes using transparent lexical scoring and return source references.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Design and safety

The core is deterministic and framework-independent. Inputs are validated, outputs retain evidence or source references, and no repository changes, deployments, notifications, or other side effects are performed. Treat findings as review assistance, not authoritative security or correctness decisions.

## Limitations

This is a bounded local reference implementation. It does not call an LLM or external service; production integrations should add authenticated adapters, telemetry, access controls, and human review.

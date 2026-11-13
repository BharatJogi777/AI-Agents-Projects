# Agent identity and authorization demo

Demonstrates identity-bound authorization with explicit action scopes, expiry, and default denial.

## Design

This project is a deterministic, dependency-light security control example. It evaluates explicit inputs and returns structured findings; it does not connect to external systems or perform privileged actions.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

## Scope and limitations

Use this as a reference implementation and extend it with authenticated identity, durable storage, observability, and integration-specific controls before production use. The included tests cover expected behavior and failure paths.

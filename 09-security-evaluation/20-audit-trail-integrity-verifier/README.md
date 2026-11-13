# Audit trail integrity verifier

Verifies a tamper-evident, hash-chained audit log and identifies the first broken link.

## Design

This deterministic example uses canonical JSON and SHA-256 to chain events. It is an integrity check, not a digital signature or proof of who created an event.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

## Production considerations

Protect signing keys and storage separately, enforce append-only permissions, define canonical serialization across implementations, and anchor checkpoints outside the log. The tests cover append, verification, tampering, and refusal to extend a broken chain.

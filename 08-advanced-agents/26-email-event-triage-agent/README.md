# Email Event Triage Agent

Normalize inbound email events, detect duplicate message identifiers, and prioritize review without modifying a mailbox.

## Safety boundary
This deterministic module analyzes supplied records only. It does not perform external actions or change source-system state.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

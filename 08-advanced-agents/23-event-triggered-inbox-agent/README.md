# Event Triggered Inbox Agent

Deduplicate inbound message events and produce cautious triage recommendations without sending, deleting, or forwarding messages.

## Safety boundary
This deterministic reference implementation validates supplied data and prepares a reviewable result. It does not autonomously contact external services or execute consequential actions.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

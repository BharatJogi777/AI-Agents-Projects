# Webhook Triggered Workflow Agent

Verify signed webhook envelopes, reject stale or replayed events, and map approved event types to workflow intents without executing them.

## Safety boundary
The module verifies HMAC signatures and returns an intent only. Persist event IDs atomically in production and execute downstream actions through separately authorized workers.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

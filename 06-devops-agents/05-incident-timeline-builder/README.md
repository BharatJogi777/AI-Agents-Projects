# Incident timeline builder

Normalize timestamped events from logs, monitoring, and incident notes into a deterministic UTC timeline.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Safety and limitations

Input-only transformation; no production connections or incident actions. Timestamps must include a timezone. Validate source authenticity and clock skew before using the timeline for post-incident conclusions.

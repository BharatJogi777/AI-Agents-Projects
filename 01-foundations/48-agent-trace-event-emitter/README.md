# AG-048 — Agent trace event emitter

A small structured event emitter with per-instance sequence numbers, UTC timestamps, bounded attributes, and sensitive-name redaction.

## Run

Python 3.12+ is recommended.

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Scope and limitations

This is not OpenTelemetry and sequence numbers are not distributed trace IDs. Add exporters, sampling, retention, and governance for production.

The implementation is intentionally small so its control flow can be inspected. Tests are included but must be run locally before treating this project as verified.

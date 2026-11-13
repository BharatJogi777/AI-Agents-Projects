# Call quality analysis assistant

## Purpose
Evaluate supplied packet loss, latency, and jitter metrics against explicit thresholds.

## Scope
Deterministic metric analysis only; no call recording, audio interpretation, or network probing.

## Run
Python 3.10+.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
Thresholds are configurable in the implementation. Results are technical indicators, not a complete measure of conversational quality.

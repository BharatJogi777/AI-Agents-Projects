# Audio Video Meeting Assistant

Synchronize independently supplied transcript, audio, and video markers on a shared timeline while surfacing gaps and conflicts.

## Safety boundary
This deterministic reference implementation validates supplied data and prepares a reviewable result. It does not autonomously contact external services or execute consequential actions.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

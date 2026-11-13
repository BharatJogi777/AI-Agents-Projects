# Daily Briefing Agent

Assemble a concise daily briefing from explicitly supplied calendar, task, and update items while retaining source attribution.

## Safety boundary
The module uses only supplied data and explicit scoring rules. It does not access personal accounts, invent events, or perform tasks.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

# Personal Task Prioritization Assistant

Rank tasks using explicit user-provided urgency, impact, effort, and due-date signals with explainable scoring.

## Safety boundary
The module uses only supplied data and explicit scoring rules. It does not access personal accounts, invent events, or perform tasks.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

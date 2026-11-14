# AG-480: Email inbox prioritization assistant

Prioritize supplied email metadata with transparent scoring rules.

## Scope and limitations

This utility processes metadata only. It does not connect to an inbox, read message bodies, send, archive, or delete messages. Priority scores are heuristics and should not replace human judgment.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

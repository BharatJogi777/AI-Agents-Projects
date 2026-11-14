# Email thread summarizer

A deterministic reference implementation for email thread summarizer using only caller-supplied information.

## Scope and limitations

This project does not connect to external accounts or send messages. Extracted content and heuristic classifications require human review. No external action is taken automatically.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

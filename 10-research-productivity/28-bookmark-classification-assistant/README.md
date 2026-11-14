# Bookmark classification assistant

A deterministic reference implementation for bookmark classification assistant.

## Scope and limitations

Processes only caller-supplied records. It does not modify, delete, send, or publish external data. Heuristic outputs require human review before consequential use.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

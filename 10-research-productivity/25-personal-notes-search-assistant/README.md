# AG-475: Personal notes search assistant

Search a caller-provided collection of personal notes using transparent keyword matching and ranked results.

## Scope and limitations

This deterministic reference implementation searches only notes explicitly supplied by the caller. It does not connect to a personal account, infer missing context, or send note contents elsewhere. Keyword overlap is not semantic understanding; review results before relying on them.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

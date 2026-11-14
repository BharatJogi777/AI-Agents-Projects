# AG-471: Executive briefing generator

Create a decision-oriented executive briefing from supplied updates, metrics, risks, and decisions needed.

## Scope and limitations

This deterministic reference implementation processes only caller-supplied information. It does not browse external sources, establish factual or legal correctness, or take external actions. Review outputs before operational or executive use.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

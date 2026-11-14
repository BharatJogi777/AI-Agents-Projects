# AG-472: Policy document comparison assistant

Compare two supplied policy revisions by section and identify additions, removals, and changed wording.

## Scope and limitations

This deterministic reference implementation processes only caller-supplied information. It does not browse external sources, establish factual or legal correctness, or take external actions. Review outputs before operational or executive use.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

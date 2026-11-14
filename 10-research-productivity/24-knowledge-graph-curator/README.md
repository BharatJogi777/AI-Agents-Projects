# AG-474: Knowledge graph curator

Validate and curate a small knowledge graph with duplicate, dangling-reference, and self-loop diagnostics.

## Scope and limitations

This deterministic reference implementation processes only caller-supplied information. It does not browse external sources, establish factual or legal correctness, or take external actions. Review outputs before operational or executive use.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

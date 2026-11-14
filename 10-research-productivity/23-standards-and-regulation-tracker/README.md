# AG-473: Standards and regulation tracker

Track supplied standards and regulation records, detect version or status changes, and flag review needs.

## Scope and limitations

This deterministic reference implementation processes only caller-supplied information. It does not browse external sources, establish factual or legal correctness, or take external actions. Review outputs before operational or executive use.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

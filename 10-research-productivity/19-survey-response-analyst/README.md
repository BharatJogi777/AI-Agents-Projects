# AG-469: Survey response analyst

Analyze structured survey responses with transparent counts, distributions, and missing-data reporting.

## Scope and limitations

This is a deterministic reporting utility, not an autonomous research system. It uses only caller-supplied records, preserves source labels where provided, and does not validate the truth of external data. Review findings and caveats before distribution.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

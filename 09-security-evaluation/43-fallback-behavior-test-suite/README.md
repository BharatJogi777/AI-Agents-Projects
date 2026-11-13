# Fallback behavior test suite

**Project ID:** AG-443

## Purpose
Validate ordered fallback attempts, success selection, and exhaustion outcomes for resilient agent services.

## Design
A deterministic Python evaluation utility. It consumes caller-provided measurements or outcomes and does not call external models, APIs, or services.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
pytest
```

## Limitations
Use representative test data and review assumptions before using results for production release decisions. This package is an evaluation aid, not a reliability guarantee.

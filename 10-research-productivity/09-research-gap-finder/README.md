# Research gap finder

## Purpose
A deterministic research utility that analyzes caller-supplied metadata. It does not crawl scholarly databases or infer facts absent from the input.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design
- Pure Python functions with immutable result objects.
- Input validation and explicit unknown/missing data.
- No network access or external side effects.

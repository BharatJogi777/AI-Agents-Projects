# Build failure investigator

## Purpose
Classify common build-log signatures into reviewable investigation steps. This tool does not execute builds or claim a root cause from log text alone.

## Run
```bash
python -m pip install -e '.[dev]'
pytest
```

## API
Call `investigate(log)` from `app/build_failure.py`. It returns matched categories, evidence tokens, and next-step suggestions.

## Limitations and safety
Log signatures are incomplete and can be misleading. The first reported symptom may be downstream of the real failure; inspect full logs, environment, and reproducibility before changing a build.

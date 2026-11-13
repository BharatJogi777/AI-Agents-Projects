# Changelog generator

## Purpose
A deterministic developer utility that transforms explicit inputs into reviewable output. It never commits, merges, or publishes changes automatically.

## Run
```bash
python -m pip install -e '.[dev]'
pytest
```

## API
See `app/changelog.py` for the public function and input/output contract.

## Limitations and safety
Review generated content before publishing. The output is a draft/checklist, not a substitute for repository history, release policy, or owner approval.

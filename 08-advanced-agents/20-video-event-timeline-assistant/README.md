# Video event timeline assistant

## Purpose
Validate timestamped video event annotations and produce a searchable timeline.

## Scope
Consumes annotations from a separate video or human review adapter. It does not decode video or infer events.

## Run
Python 3.10+.
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Safety
Preserve provenance and confidence values. Validate timestamps against actual media duration and review low-confidence annotations before operational use.

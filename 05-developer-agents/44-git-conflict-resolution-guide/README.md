# Git conflict resolution guide

## Purpose
Create a cautious manual resolution checklist from structured Git conflict metadata. It never edits the working tree or selects a winning side automatically.

## Run
```bash
python -m pip install -e '.[dev]'
pytest
```

## API
Use `guide` in `app/conflict_guide.py` with a list of conflict records containing `path` and optional `kind` (`content`, `rename`, `delete_modify`, or `binary`).

## Safety
Deletion/modification and binary conflicts require human decisions. Inspect history, verify intended behavior, run tests, and review the final diff before committing.

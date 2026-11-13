# Patch Validation Agent

Validates unified diffs before they are handed to a human reviewer. Checks patch structure, whitespace errors, suspicious absolute paths, and binary/rename indicators without applying or executing the patch.

## Run
```bash
pip install -e ".[dev]"
python -m app.validate_patch
pytest
```

## Limitations
This is a lightweight preflight validator, not a complete Git implementation. Run `git apply --check` in a controlled checkout for authoritative applicability checks.

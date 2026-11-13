# Patch Generation Assistant

Generates a unified diff for a narrowly scoped text replacement. The tool validates the expected old content, rejects ambiguous matches by default, and returns a patch for review instead of writing to disk.

## Run
```bash
pip install -e ".[dev]"
python -m app.patch
pytest
```

## Safety
No filesystem writes occur. Review the generated diff, inspect surrounding context, and run tests before applying it.

# Regression Test Selector

Ranks existing tests for a changed-file set using explicit test-to-source mappings. Selection is explainable and deterministic; unmapped changes are called out rather than silently ignored.

## Run
```bash
pip install -e ".[dev]"
python -m app.selector
pytest
```

## Limitations
The selector does not parse arbitrary dependency graphs or execute tests. Keep the mapping current and run the complete suite when impact is uncertain.

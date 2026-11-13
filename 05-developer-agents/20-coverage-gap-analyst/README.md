# Coverage Gap Analyst

Compares declared source modules with a coverage.py JSON report and ranks modules by missing executable lines. It highlights unmeasured modules separately from measured low-coverage modules.

## Run
```bash
pip install -e ".[dev]"
python -m app.coverage
pytest
```

Generate input using `coverage json -o coverage.json`.

## Limitations
Coverage measures execution, not assertion quality. Use branch coverage and mutation testing where appropriate; exclude generated/vendor files deliberately rather than hiding meaningful gaps.

# Golden dataset regression runner

Golden dataset regression runner is a deterministic, provider-independent evaluation utility. Supply explicit reference labels or templates; results are reproducible and inspectable.

## Run

```bash
python -m pip install -e ".[dev]"
pytest
```

## Limitations

Synthetic and heuristic evaluations do not establish real-world model quality. Validate representative datasets and keep human review for consequential decisions.

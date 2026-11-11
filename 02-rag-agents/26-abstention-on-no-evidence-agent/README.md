# AG-76 — Abstention-on-no-evidence agent

Return an explicit abstention when retrieved evidence is absent or below a configured confidence threshold.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Safety and limitations

This project provides deterministic graph/retrieval policy primitives. Model extraction and answer generation are injected responsibilities; preserve source IDs throughout the pipeline.

Tests are authored but have not been run locally.

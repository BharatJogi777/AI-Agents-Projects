# AG-79 — Graph traversal question-answering agent

Traverse a validated directed knowledge graph with hop limits, cycle protection, and source-carrying paths.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Safety and limitations

This project provides deterministic graph/retrieval policy primitives. Model extraction and answer generation are injected responsibilities; preserve source IDs throughout the pipeline.

Tests are authored but have not been run locally.

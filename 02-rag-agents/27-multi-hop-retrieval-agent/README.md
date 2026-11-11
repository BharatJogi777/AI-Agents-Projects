# AG-77 — Multi-hop retrieval agent

Execute bounded retrieval hops where each hop derives its next query from prior retrieved evidence and records provenance.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Safety and limitations

This project provides deterministic graph/retrieval policy primitives. Model extraction and answer generation are injected responsibilities; preserve source IDs throughout the pipeline.

Tests are authored but have not been run locally.

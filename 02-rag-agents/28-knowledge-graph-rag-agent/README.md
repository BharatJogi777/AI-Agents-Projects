# AG-78 — Knowledge graph RAG agent

Represent extracted entities and relations as validated triples, then retrieve bounded connected facts for grounded context.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Safety and limitations

This project provides deterministic graph/retrieval policy primitives. Model extraction and answer generation are injected responsibilities; preserve source IDs throughout the pipeline.

Tests are authored but have not been run locally.

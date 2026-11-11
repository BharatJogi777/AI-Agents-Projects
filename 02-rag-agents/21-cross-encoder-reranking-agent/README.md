# AG-71 — Cross-encoder reranking agent

Rerank an initial retrieval candidate set with an injected query-passage relevance scorer, deterministic ties, and bounded output.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

## Safety and limitations

This project is a deterministic component with an injected model/scoring boundary where applicable. Citation checks prove source identity and exact-quote presence, not that a source logically entails a claim. Evidence coverage measures citation presence, not truth. Tests are authored but have not been run locally.

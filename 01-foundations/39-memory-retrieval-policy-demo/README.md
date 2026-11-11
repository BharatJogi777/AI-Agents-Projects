# AG-039 — Memory retrieval policy demo

Filters memory candidates by confirmation, sensitivity, expiry, and confidence, then ranks matching candidates using lexical overlap, confidence, and recency. Ranking scores are returned separately from records.

## Modules
- `memory_retrieval/contracts.py`: memory and ranked-result DTOs.
- `memory_retrieval/retriever.py`: lexical tokenization, safety filters, score calculation, deduplication, and stable ordering.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This is a transparent baseline, not semantic retrieval. Add embedding search, tenant isolation, source citations, and calibrated ranking evaluation for production. Local test execution remains pending.
# AG-57 — JSON dataset assistant

Normalize JSON objects and arrays into bounded records with stable JSON paths and canonical serialization for evidence and indexing.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

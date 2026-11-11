# AG-60 — Incremental document indexer

Maintain a transactional SQLite document and chunk index using content hashes, deterministic chunk IDs, and unchanged-document skips.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

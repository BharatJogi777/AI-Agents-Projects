# AG-59 — Directory watcher ingestion agent

Poll a document directory safely and emit deterministic created, modified, and deleted events using content hashes without following symlinks.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

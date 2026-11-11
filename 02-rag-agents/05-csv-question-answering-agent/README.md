# AG-55 — CSV question-answering agent

Turn CSV rows into evidence-bearing records with row numbers, strict headers, bounded file size, and safe handling of quoted delimiters.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

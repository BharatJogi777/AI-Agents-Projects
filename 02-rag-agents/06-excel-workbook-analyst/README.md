# AG-56 — Excel workbook analyst

Read Excel worksheets in read-only mode, preserve sheet and row provenance, and bound workbook size and row counts.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

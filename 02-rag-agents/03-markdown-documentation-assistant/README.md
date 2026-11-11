# AG-53 — Markdown documentation assistant

Split Markdown documentation into heading-aware chunks while retaining heading paths, source line ranges, and original text for citations.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

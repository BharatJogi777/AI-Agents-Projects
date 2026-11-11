# AG-52 — DOCX knowledge assistant

Extract DOCX paragraphs and table rows in document order, retaining structural labels so retrieved evidence can be traced to its source.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

# AG-51 — PDF question-answering agent

Extract page-aware text from PDF files and return bounded evidence snippets with page numbers for downstream grounded answers.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

# AG-58 — Multi-format document ingester

Provide one bounded ingestion interface for TXT, Markdown, HTML, CSV, JSON, PDF, DOCX, and XLSX while retaining source-specific provenance.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

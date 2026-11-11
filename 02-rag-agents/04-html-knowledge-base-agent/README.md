# AG-54 — HTML knowledge-base agent

Extract readable HTML text while excluding script, style, and hidden content; retain headings and links as text for safer knowledge ingestion.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

This is a deterministic ingestion component, not a complete RAG application. OCR, embeddings, vector search, access control, and grounded answer generation are separate concerns. Tests are authored but require local execution.

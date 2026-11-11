# AG-63 — Semantic chunking pipeline

Split text at injected semantic similarity boundaries while retaining source offsets.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

Semantic scoring is injected by the caller. These components do not provide embeddings or a vector database. Tests are authored but not locally executed.

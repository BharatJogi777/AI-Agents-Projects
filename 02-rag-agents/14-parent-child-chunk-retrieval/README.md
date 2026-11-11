# AG-64 — Parent-child chunk retrieval

Store larger parent passages and smaller searchable child chunks, then expand matched children to parent context.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

Semantic scoring is injected by the caller. These components do not provide embeddings or a vector database. Tests are authored but not locally executed.

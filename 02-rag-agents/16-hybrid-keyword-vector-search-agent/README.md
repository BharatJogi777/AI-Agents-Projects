# AG-66 — Hybrid keyword-vector search agent

Combine lexical and vector rankings using reciprocal rank fusion.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

The hybrid ranker expects independently ranked candidate lists from lexical and vector search providers. Tests are authored but not locally executed.

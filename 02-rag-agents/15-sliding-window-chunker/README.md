# AG-65 — Sliding-window chunker

Generate overlapping text windows with stable offsets and validated size and overlap.

## Run

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

The hybrid ranker expects independently ranked candidate lists from lexical and vector search providers. Tests are authored but not locally executed.

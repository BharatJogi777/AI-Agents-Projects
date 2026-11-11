# AG-025 — Incremental JSON stream parser

Decodes JSON values arriving in arbitrary text chunks without assuming chunk boundaries align with JSON tokens. Supports concatenated values, bounded buffering, and explicit end-of-stream validation.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This is a JSON value stream decoder, not a semantic partial-object parser. Incomplete prefixes remain buffered until more data arrives, the configured limit is reached, or `finish()` validates the final stream. Tests are authored but not yet executed.

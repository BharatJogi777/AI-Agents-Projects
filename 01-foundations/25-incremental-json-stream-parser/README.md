# AG-025 — Incremental JSON stream parser

Decodes concatenated JSON values arriving in arbitrary text chunks. It buffers incomplete prefixes, enforces a maximum pending-buffer size, and validates the final remainder when the stream closes.

## Architecture
- `json_stream/contracts.py`: dedicated stream decoding error.
- `json_stream/decoder.py`: incremental raw decoder, buffer inspection, finish validation, and reset.
- `app.py`: compatibility facade.

## Execution flow
1. Feed a text chunk.
2. Decode as many complete JSON values as possible from the start of the pending buffer.
3. Retain any incomplete suffix for the next chunk.
4. Call `finish()` at end-of-stream to reject incomplete or trailing invalid data.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This handles concatenated complete JSON values, not semantic partial-object events. The limit applies to the pending undecoded buffer. Tests are authored; local execution remains pending.

# AG-025 — Incremental JSON stream parser

A small streaming component for decoding **concatenated JSON values** from a source that delivers arbitrary text chunks. Chunk boundaries have no semantic meaning: a JSON object may arrive in one piece or be split between any two characters.

## What it does

- Emits each complete JSON value as soon as it can be decoded.
- Retains only the incomplete suffix between calls.
- Supports objects, arrays, strings, numbers, booleans, and null.
- Handles multiple values in one chunk and across chunk boundaries.
- Enforces a maximum size for the pending incomplete value.
- Validates end-of-stream with `finish()`.
- Rejects non-standard numeric constants such as `NaN` and `Infinity`.
- Requires `reset()` before reusing a finished decoder.

This is a text-level parser. If the upstream transport supplies bytes, decode them to text with a correctly configured incremental UTF-8 decoder before passing chunks here. It is not an NDJSON parser and does not require one JSON value per line.

## Project structure

```text
.
├── app.py                    # small backwards-compatible import facade
├── json_stream/
│   ├── __init__.py
│   ├── contracts.py          # parser-specific exception
│   └── decoder.py            # incremental state machine
├── tests/
│   └── test_decoder.py
├── pyproject.toml
└── README.md
```

## Install and test

Python 3.12 or newer is required.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Usage

```python
from json_stream import IncrementalJSONDecoder, IncrementalJSONError

decoder = IncrementalJSONDecoder(max_buffer_chars=64_000)

for text_chunk in incoming_text_chunks:
    for value in decoder.feed(text_chunk):
        process(value)

try:
    for final_value in decoder.finish():
        process(final_value)
except IncrementalJSONError:
    # The producer ended with a truncated or malformed JSON value.
    raise
```

## Lifecycle and limits

`feed()` returns a list because a single transport chunk can contain zero, one, or many complete values. The decoder retains a partial suffix until more text arrives. `max_buffer_chars` bounds that retained suffix, not the size of a chunk containing many already-complete values. Call `finish()` exactly at end-of-stream; after that, `feed()` raises until `reset()` starts a new stream.

The standard-library JSON decoder is used for syntax and value construction. As with any parser that receives text, this component cannot recover the original byte boundaries or validate the transport's UTF-8 decoding policy.

## Verification status

Unit tests cover arbitrary chunk splits, multiple values, malformed/truncated EOF, pending-buffer limits, JSON whitespace, non-finite numbers, and lifecycle behavior. Tests are committed but have **not yet been executed in the user's local environment**.

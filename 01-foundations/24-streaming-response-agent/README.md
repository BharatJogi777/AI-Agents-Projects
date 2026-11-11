# AG-024 — Streaming response agent

A transport-independent parser for fragmented Server-Sent Events from an OpenAI-compatible chat-completions stream. It emits incremental text events and recognizes finish reasons and the `[DONE]` sentinel.

## Architecture
- `sse_parser/contracts.py`: stream event and protocol error types.
- `sse_parser/parser.py`: incremental frame buffering, SSE data-line parsing, JSON validation, terminal-state handling, and frame-size limits.
- `app.py`: compatibility facade.

## Execution flow
Feed arbitrary text chunks. Complete frames are parsed as they become available; partial frames remain buffered. Comments are ignored, multi-line `data:` fields are joined, malformed JSON/shape is rejected, and content after a terminal event is not accepted.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This parser does not open HTTP connections. Transport backpressure, disconnect handling, retry policy, and cancellation belong to the caller. Tests are authored; local execution remains pending.

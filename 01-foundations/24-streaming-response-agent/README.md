# AG-024 — Streaming response agent

A transport-independent SSE parser consumes fragmented text chunks and emits incremental assistant text and terminal events. It handles multiple frames per chunk, partial frames, malformed JSON, and the `[DONE]` sentinel.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

This implements a common OpenAI-compatible chat-completions event shape. HTTP streaming, backpressure, retries, and cancellation belong to the transport layer. Tests are authored but not yet executed.

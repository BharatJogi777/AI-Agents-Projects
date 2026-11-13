# AG-024 — Streaming response agent

A transport-independent parser for fragmented Server-Sent Events (SSE) from an OpenAI-compatible chat-completions stream. It emits incremental text events and recognizes finish reasons and the [DONE] sentinel.

## Architecture

- sse_parser/contracts.py: immutable stream event and protocol error types.
- sse_parser/parser.py: incremental frame buffering, SSE data-line parsing, JSON validation, terminal-state handling, and frame-size limits.
- sse_parser/streaming.py: async iterator adapter that yields parsed events immediately and closes the provider iterator on normal completion, failure, or consumer cancellation.
- app.py: backward-compatible import facade.

## Execution flow

The transport layer creates the HTTP response and exposes its text chunks. Pass those chunks to iter_chat_events(). Complete frames are parsed as they arrive; incomplete frames remain buffered. Provider exceptions and cancellation propagate to the caller. The adapter closes the underlying async iterator when it supports aclose(), including when the consumer disconnects or stops iteration early.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Example

```python
import httpx
from sse_parser import iter_chat_events

async def consume(response: httpx.Response) -> None:
    async for event in iter_chat_events(response.aiter_text()):
        if event.text:
            print(event.text, end="", flush=True)
        if event.finished:
            break
```

Use the adapter inside the lifetime of the HTTP response context manager. Do not return the iterator after its response has been closed.

## Boundaries and operational notes

- This package does not create HTTP connections, retry requests, or own authentication.
- Configure connect/read timeouts and response-size limits in the HTTP transport.
- Do not retry after yielding partial output unless the application has an explicit deduplication/resume strategy.
- A consumer disconnect should close the async iterator and its owning HTTP response context.
- The parser's frame limit bounds buffered incomplete input; the transport should also enforce total response and duration budgets.
- Tests use in-memory async iterators and require no model or API key.

Tests are authored; local execution remains pending.

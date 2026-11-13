"""Async streaming lifecycle helpers for provider-neutral text chunks.

The transport owns HTTP response creation. This module owns incremental parsing
and deterministic closure of the supplied async iterator.
"""
from __future__ import annotations

from collections.abc import AsyncIterable, AsyncIterator

from .contracts import StreamEvent
from .parser import ChatCompletionStreamParser


async def iter_chat_events(
    chunks: AsyncIterable[str],
    *,
    parser: ChatCompletionStreamParser | None = None,
) -> AsyncIterator[StreamEvent]:
    """Convert an async text-chunk stream into incremental chat events.

    The source iterator is closed in finally when it supports aclose.
    Cancellation and provider exceptions are deliberately propagated to the
    caller; this helper never silently retries or hides a partial response.
    """
    active_parser = parser or ChatCompletionStreamParser()
    iterator = aiter(chunks)
    try:
        async for chunk in iterator:
            for event in active_parser.feed(chunk):
                yield event
            if active_parser.finished:
                return
        for event in active_parser.close():
            yield event
    finally:
        close = getattr(iterator, "aclose", None)
        if close is not None:
            await close()

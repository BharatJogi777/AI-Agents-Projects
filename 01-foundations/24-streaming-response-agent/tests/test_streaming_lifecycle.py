import asyncio
import json

import pytest

from sse_parser import StreamEvent
from sse_parser.streaming import iter_chat_events


def frame(content: str) -> str:
    payload = {"choices": [{"delta": {"content": content}, "finish_reason": None}]}
    return "data: " + json.dumps(payload) + "\n\n"


class Source:
    def __init__(self, chunks):
        self.chunks = iter(chunks)
        self.closed = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.chunks)
        except StopIteration:
            raise StopAsyncIteration

    async def aclose(self):
        self.closed = True


def test_incremental_events_and_source_cleanup():
    async def scenario():
        source = Source([frame("Hel")[:8], frame("Hel")[8:] + frame("lo")])
        events = [event async for event in iter_chat_events(source)]
        assert "".join(event.text for event in events) == "Hello"
        assert source.closed
    asyncio.run(scenario())


def test_terminal_event_stops_consuming_source():
    async def scenario():
        source = Source(["data: [DONE]\n\n", frame("must not be read")])
        events = [event async for event in iter_chat_events(source)]
        assert events == [StreamEvent("", True, "stop")]
        assert source.closed
    asyncio.run(scenario())


def test_provider_failure_is_not_hidden_and_source_is_closed():
    class Broken:
        def __init__(self):
            self.closed = False
            self.count = 0

        def __aiter__(self):
            return self

        async def __anext__(self):
            self.count += 1
            if self.count == 1:
                return frame("partial")
            raise RuntimeError("provider disconnected")

        async def aclose(self):
            self.closed = True

    async def scenario():
        source = Broken()
        with pytest.raises(RuntimeError, match="provider disconnected"):
            _ = [event async for event in iter_chat_events(source)]
        assert source.closed
    asyncio.run(scenario())


def test_consumer_cancellation_closes_source():
    async def scenario():
        source = Source([frame("one"), frame("two"), frame("three")])
        iterator = iter_chat_events(source)
        await anext(iterator)
        await iterator.aclose()
        assert source.closed
    asyncio.run(scenario())

import pytest
from app.reconnecting import ReconnectingClient


@pytest.mark.asyncio
async def test_retries_transient_error_then_succeeds():
    calls, delays = 0, []
    async def sleep(delay):
        delays.append(delay)
    async def operation():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise ConnectionError("temporary")
        return "ok"
    client = ReconnectingClient(
        transient_errors=(ConnectionError,), attempts=3,
        base_delay=0.1, jitter=0, sleep=sleep,
    )
    assert await client.execute(operation) == "ok"
    assert calls == 3
    assert delays == [0.1, 0.2]


@pytest.mark.asyncio
async def test_does_not_retry_unclassified_errors():
    calls = 0
    async def operation():
        nonlocal calls
        calls += 1
        raise ValueError("invalid tool input")
    client = ReconnectingClient(transient_errors=(ConnectionError,), attempts=4)
    with pytest.raises(ValueError):
        await client.execute(operation)
    assert calls == 1


@pytest.mark.asyncio
async def test_exhaustion_reraises_last_connection_error():
    async def operation():
        raise ConnectionError("offline")
    client = ReconnectingClient(transient_errors=(ConnectionError,), attempts=2, sleep=lambda _: asyncio.sleep(0))
    with pytest.raises(ConnectionError, match="offline"):
        await client.execute(operation)

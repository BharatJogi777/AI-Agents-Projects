import asyncio
import math

import pytest

from app import (
    RequestDeadlineExceeded,
    ToolTimedOut,
    execute_with_timeout,
)


def test_async_handler_completes_before_deadline():
    async def handler(value):
        await asyncio.sleep(0.001)
        return value * 2

    result = asyncio.run(execute_with_timeout(handler, 4, timeout_seconds=1))
    assert result.ok
    assert result.value == 8
    assert result.elapsed_seconds >= 0


def test_slow_handler_is_cancelled_on_tool_timeout():
    cancelled = []

    async def handler():
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            cancelled.append(True)
            raise

    async def run():
        with pytest.raises(ToolTimedOut):
            await execute_with_timeout(handler, timeout_seconds=0.01)

    asyncio.run(run())
    assert cancelled == [True]


def test_request_deadline_wins_when_earlier_than_tool_timeout():
    async def handler():
        await asyncio.sleep(1)

    async def run():
        loop = asyncio.get_running_loop()
        with pytest.raises(RequestDeadlineExceeded):
            await execute_with_timeout(
                handler,
                timeout_seconds=1,
                deadline_at=loop.time() + 0.01,
            )

    asyncio.run(run())


def test_tool_timeout_wins_when_request_deadline_is_later():
    async def handler():
        await asyncio.sleep(1)

    async def run():
        loop = asyncio.get_running_loop()
        with pytest.raises(ToolTimedOut):
            await execute_with_timeout(
                handler,
                timeout_seconds=0.01,
                deadline_at=loop.time() + 1,
            )

    asyncio.run(run())


def test_already_expired_request_deadline_does_not_call_handler():
    calls = []

    async def handler():
        calls.append(True)

    async def run():
        loop = asyncio.get_running_loop()
        with pytest.raises(RequestDeadlineExceeded):
            await execute_with_timeout(
                handler, timeout_seconds=1, deadline_at=loop.time() - 1
            )

    asyncio.run(run())
    assert calls == []


def test_handler_raised_timeout_is_not_misclassified():
    async def handler():
        raise TimeoutError("upstream timed out")

    with pytest.raises(TimeoutError, match="upstream timed out") as error:
        asyncio.run(execute_with_timeout(handler, timeout_seconds=1))
    assert not isinstance(error.value, ToolTimedOut)


def test_handler_exception_propagates():
    async def handler():
        raise RuntimeError("failure")

    with pytest.raises(RuntimeError, match="failure"):
        asyncio.run(execute_with_timeout(handler, timeout_seconds=1))


def test_external_cancellation_propagates_to_handler():
    cancelled = asyncio.Event()
    started = asyncio.Event()

    async def handler():
        started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            cancelled.set()
            raise

    async def run():
        task = asyncio.create_task(
            execute_with_timeout(handler, timeout_seconds=10)
        )
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert cancelled.is_set()

    asyncio.run(run())


def test_async_callable_object_is_supported():
    class Handler:
        async def __call__(self, value):
            return value + 1

    result = asyncio.run(execute_with_timeout(Handler(), 2, timeout_seconds=1))
    assert result.value == 3


@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf"), True, 301])
def test_timeout_bounds_are_validated(timeout):
    async def handler():
        return None

    with pytest.raises(ValueError):
        asyncio.run(execute_with_timeout(handler, timeout_seconds=timeout))


def test_sync_handler_is_rejected():
    with pytest.raises(TypeError, match="async"):
        asyncio.run(execute_with_timeout(lambda: None, timeout_seconds=1))


def test_invalid_deadline_is_rejected():
    async def handler():
        return None

    for deadline in (True, float("nan"), float("inf")):
        with pytest.raises(ValueError):
            asyncio.run(
                execute_with_timeout(
                    handler, timeout_seconds=1, deadline_at=deadline
                )
            )

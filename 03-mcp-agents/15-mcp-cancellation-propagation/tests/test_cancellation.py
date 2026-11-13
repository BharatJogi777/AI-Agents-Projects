import asyncio
import pytest
from app.cancellation import cancellable_sleep, run_with_cancellation


@pytest.mark.asyncio
async def test_shared_event_cancels_downstream_work():
    event = asyncio.Event()
    async def operation(signal):
        await cancellable_sleep(10, signal)
        return "unexpected"
    task = asyncio.create_task(run_with_cancellation(operation, cancellation=event))
    await asyncio.sleep(0)
    event.set()
    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_task_cancellation_sets_signal():
    event = asyncio.Event()
    started = asyncio.Event()
    async def operation(signal):
        started.set()
        await cancellable_sleep(30, signal)
    task = asyncio.create_task(run_with_cancellation(operation, cancellation=event))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert event.is_set()


@pytest.mark.asyncio
async def test_sleep_completes_without_cancellation():
    await cancellable_sleep(0.001, asyncio.Event())

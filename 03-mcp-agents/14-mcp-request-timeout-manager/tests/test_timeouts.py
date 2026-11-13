import asyncio
import pytest
from app.timeouts import RequestTimeoutManager, TimeoutPolicy


@pytest.mark.asyncio
async def test_operation_completes_within_timeout():
    manager = RequestTimeoutManager(TimeoutPolicy(1, 3))
    assert await manager.run(lambda: asyncio.sleep(0, result="done")) == "done"


@pytest.mark.asyncio
async def test_slow_operation_times_out():
    manager = RequestTimeoutManager(TimeoutPolicy(0.01, 1))
    with pytest.raises(TimeoutError):
        await manager.run(lambda: asyncio.sleep(1))


def test_requested_timeout_is_capped():
    policy = TimeoutPolicy(2, 5)
    assert policy.resolve(100) == 5


@pytest.mark.asyncio
async def test_expired_deadline_fails_before_operation():
    manager = RequestTimeoutManager(TimeoutPolicy(1, 2))
    called = False
    async def operation():
        nonlocal called
        called = True
    with pytest.raises(TimeoutError):
        await manager.run(operation, deadline=asyncio.get_running_loop().time() - 1)
    assert not called

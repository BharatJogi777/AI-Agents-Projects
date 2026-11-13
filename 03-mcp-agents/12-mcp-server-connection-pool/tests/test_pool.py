import asyncio
import pytest

from app.pool import SessionPool


@pytest.mark.asyncio
async def test_pool_reuses_session_after_lease():
    created = []
    async def factory():
        session = object()
        created.append(session)
        return session
    async def close(_session):
        pass

    pool = SessionPool(factory, close, max_size=1)
    async with pool.acquire() as first:
        assert first is created[0]
    async with pool.acquire() as second:
        assert second is first
    assert len(created) == 1
    await pool.close()


@pytest.mark.asyncio
async def test_pool_enforces_capacity_and_waits_for_release():
    active, peak = 0, 0
    async def factory():
        return object()
    async def close(_session):
        pass
    pool = SessionPool(factory, close, max_size=1)
    async def worker():
        nonlocal active, peak
        async with pool.acquire():
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.02)
            active -= 1
    await asyncio.gather(worker(), worker(), worker())
    assert peak == 1
    await pool.close()


@pytest.mark.asyncio
async def test_pool_rejects_invalid_capacity():
    with pytest.raises(ValueError):
        SessionPool(lambda: None, lambda _: None, max_size=0)

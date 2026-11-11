import asyncio
import pytest
from app import execute_with_timeout,ToolTimedOut


def test_async_handler_completes_before_deadline():
    async def handler(x): await asyncio.sleep(0.001); return x*2
    result=asyncio.run(execute_with_timeout(handler,4,timeout_seconds=1))
    assert result.ok and result.value==8 and result.elapsed_seconds>=0


def test_slow_handler_is_cancelled_on_timeout():
    cancelled=[]
    async def handler():
        try: await asyncio.sleep(1)
        except asyncio.CancelledError:
            cancelled.append(True)
            raise
    async def run():
        with pytest.raises(ToolTimedOut):
            await execute_with_timeout(handler,timeout_seconds=0.01)
    asyncio.run(run())
    assert cancelled==[True]


def test_timeout_bounds_and_handler_type():
    async def handler(): return "ok"
    with pytest.raises(ValueError): asyncio.run(execute_with_timeout(handler,timeout_seconds=0))
    with pytest.raises(TypeError): asyncio.run(execute_with_timeout(lambda:None,timeout_seconds=1))


def test_handler_exception_propagates():
    async def handler(): raise RuntimeError("failure")
    with pytest.raises(RuntimeError,match="failure"):
        asyncio.run(execute_with_timeout(handler,timeout_seconds=1))

"""Timeout wrapper for async tool handlers with explicit cancellation semantics."""
import asyncio
from dataclasses import dataclass
from typing import Any, Awaitable, Callable


class ToolTimedOut(TimeoutError): pass


@dataclass(frozen=True)
class TimeoutResult:
    ok: bool
    value: Any = None
    error: str | None = None
    elapsed_seconds: float = 0.0


async def execute_with_timeout(handler: Callable[..., Awaitable[Any]], *args,
                               timeout_seconds: float, **kwargs) -> TimeoutResult:
    if timeout_seconds <= 0 or timeout_seconds > 300:
        raise ValueError("timeout_seconds must be greater than 0 and at most 300")
    if not asyncio.iscoroutinefunction(handler):
        raise TypeError("handler must be an async function")
    loop=asyncio.get_running_loop()
    started=loop.time()
    task=asyncio.create_task(handler(*args,**kwargs))
    try:
        value=await asyncio.wait_for(task,timeout=timeout_seconds)
        return TimeoutResult(True,value=value,elapsed_seconds=loop.time()-started)
    except asyncio.TimeoutError as exc:
        # wait_for cancels the task; handlers should cooperate with cancellation.
        raise ToolTimedOut(f"tool exceeded {timeout_seconds:.3f}s timeout") from exc

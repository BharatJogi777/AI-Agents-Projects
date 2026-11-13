"""Propagate caller cancellation through a composed async operation."""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def run_with_cancellation(
    operation: Callable[[asyncio.Event], Awaitable[T]],
    *,
    cancellation: asyncio.Event | None = None,
) -> T:
    """Run operation with a shared cancellation signal.

    The operation must observe the event and pass it to downstream work.
    Cancelling this coroutine also cancels the operation task.
    """
    signal = cancellation or asyncio.Event()
    task = asyncio.create_task(operation(signal))
    try:
        return await task
    except asyncio.CancelledError:
        signal.set()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        raise


async def cancellable_sleep(seconds: float, cancellation: asyncio.Event) -> None:
    if seconds < 0:
        raise ValueError("seconds cannot be negative")
    try:
        await asyncio.wait_for(cancellation.wait(), timeout=seconds)
    except TimeoutError:
        return
    raise asyncio.CancelledError("operation cancellation requested")

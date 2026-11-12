"""Async tool execution with per-tool and optional request deadlines."""
from __future__ import annotations

import asyncio
import inspect
import math
from dataclasses import dataclass
from typing import Any, Awaitable, Callable


from .errors import RequestDeadlineExceeded, ToolTimedOut


@dataclass(frozen=True, slots=True)
class TimeoutResult:
    ok: bool
    value: Any = None
    error: str | None = None
    elapsed_seconds: float = 0.0


def _validate_timeout(timeout_seconds: float) -> float:
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)):
        raise ValueError("timeout_seconds must be a finite number")
    value = float(timeout_seconds)
    if not math.isfinite(value) or not 0 < value <= 300:
        raise ValueError("timeout_seconds must be greater than 0 and at most 300")
    return value


def _is_async_callable(handler: Any) -> bool:
    return inspect.iscoroutinefunction(handler) or inspect.iscoroutinefunction(
        getattr(handler, "__call__", None)
    )


async def execute_with_timeout(
    handler: Callable[..., Awaitable[Any]],
    *args: Any,
    timeout_seconds: float,
    deadline_at: float | None = None,
    **kwargs: Any,
) -> TimeoutResult:
    """Run one async tool call with a monotonic per-tool timeout.

    Args:
        handler: An async function or async callable object.
        *args/**kwargs: Arguments passed directly to the handler.
        timeout_seconds: Per-tool timeout, strictly greater than zero and
            capped at five minutes.
        deadline_at: Optional absolute deadline from loop.time(). If supplied,
            the earlier of the tool timeout and request deadline wins.

    Raises:
        ToolTimedOut: The per-tool timeout elapsed.
        RequestDeadlineExceeded: The request-wide deadline elapsed first.
        asyncio.CancelledError: The caller cancelled this execution.
        Exception: Exceptions raised by the handler are propagated unchanged.
    """
    timeout = _validate_timeout(timeout_seconds)
    if not _is_async_callable(handler):
        raise TypeError("handler must be an async function or async callable")

    loop = asyncio.get_running_loop()
    started = loop.time()

    if deadline_at is not None:
        if isinstance(deadline_at, bool) or not isinstance(deadline_at, (int, float)):
            raise ValueError("deadline_at must be a finite monotonic timestamp")
        deadline = float(deadline_at)
        if not math.isfinite(deadline):
            raise ValueError("deadline_at must be a finite monotonic timestamp")
        remaining = deadline - started
        if remaining <= 0:
            raise RequestDeadlineExceeded("request deadline already elapsed")
    else:
        remaining = None

    request_deadline_wins = remaining is not None and remaining <= timeout
    effective_timeout = min(timeout, remaining) if remaining is not None else timeout

    timeout_scope = asyncio.timeout(effective_timeout)
    try:
        async with timeout_scope:
            value = await handler(*args, **kwargs)
    except TimeoutError as exc:
        # The context manager exposes whether it initiated cancellation. This
        # avoids misclassifying a TimeoutError raised by the handler itself.
        if not timeout_scope.expired():
            raise
        elapsed = loop.time() - started
        if request_deadline_wins:
            raise RequestDeadlineExceeded(
                f"request deadline elapsed while tool was running ({elapsed:.3f}s)"
            ) from exc
        raise ToolTimedOut(
            f"tool exceeded its {timeout:.3f}s timeout ({elapsed:.3f}s)"
        ) from exc

    return TimeoutResult(
        ok=True,
        value=value,
        elapsed_seconds=loop.time() - started,
    )

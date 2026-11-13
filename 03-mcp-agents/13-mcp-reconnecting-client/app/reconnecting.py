"""Reconnect wrapper with bounded exponential backoff.

The injected operation should perform one MCP request using a live session.
Only explicitly configured transient failures are retried. Tool/application
errors should normally be excluded from transient_errors.
"""
from __future__ import annotations

import asyncio
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")
Operation = Callable[[], Awaitable[T]]


class ReconnectingClient:
    def __init__(
        self,
        *,
        transient_errors: tuple[type[Exception], ...],
        attempts: int = 3,
        base_delay: float = 0.1,
        max_delay: float = 2.0,
        jitter: float = 0.1,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        random_value: Callable[[], float] = random.random,
    ) -> None:
        if attempts < 1 or base_delay < 0 or max_delay < base_delay:
            raise ValueError("invalid retry limits")
        if not 0 <= jitter <= 1:
            raise ValueError("jitter must be between 0 and 1")
        self.transient_errors = transient_errors
        self.attempts, self.base_delay = attempts, base_delay
        self.max_delay, self.jitter = max_delay, jitter
        self._sleep, self._random = sleep, random_value

    async def execute(self, operation: Operation[T]) -> T:
        for attempt in range(self.attempts):
            try:
                return await operation()
            except self.transient_errors:
                if attempt == self.attempts - 1:
                    raise
                delay = min(self.max_delay, self.base_delay * (2 ** attempt))
                delay *= 1 + self.jitter * (2 * self._random() - 1)
                await self._sleep(max(0.0, delay))
        raise AssertionError("unreachable")

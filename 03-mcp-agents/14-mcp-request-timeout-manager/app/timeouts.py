"""Per-request timeout policy with an optional end-to-end deadline."""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class TimeoutPolicy:
    default_seconds: float
    maximum_seconds: float

    def __post_init__(self) -> None:
        if self.default_seconds <= 0 or self.maximum_seconds <= 0:
            raise ValueError("timeouts must be positive")
        if self.default_seconds > self.maximum_seconds:
            raise ValueError("default timeout cannot exceed maximum")

    def resolve(self, requested: float | None = None, *, remaining: float | None = None) -> float:
        timeout = self.default_seconds if requested is None else requested
        if timeout <= 0:
            raise ValueError("requested timeout must be positive")
        timeout = min(timeout, self.maximum_seconds)
        if remaining is not None:
            if remaining <= 0:
                raise TimeoutError("request deadline has expired")
            timeout = min(timeout, remaining)
        return timeout


class RequestTimeoutManager:
    def __init__(self, policy: TimeoutPolicy) -> None:
        self.policy = policy

    async def run(
        self,
        operation: Callable[[], Awaitable[T]],
        *,
        requested: float | None = None,
        deadline: float | None = None,
    ) -> T:
        loop = asyncio.get_running_loop()
        remaining = None if deadline is None else deadline - loop.time()
        timeout = self.policy.resolve(requested, remaining=remaining)
        async with asyncio.timeout(timeout):
            return await operation()

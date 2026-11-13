"""A bounded async pool for caller-created MCP client sessions.

The pool owns leases, not transport construction. Supply a factory that returns
an already-connected session and a close callback appropriate to its transport.
"""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator


SessionFactory = Callable[[], Awaitable[Any]]
SessionCloser = Callable[[Any], Awaitable[None]]


@dataclass
class _Entry:
    session: Any
    in_use: bool = False


class SessionPool:
    def __init__(
        self,
        factory: SessionFactory,
        close: SessionCloser,
        *,
        max_size: int = 4,
        acquire_timeout: float = 5.0,
    ) -> None:
        if max_size < 1 or acquire_timeout <= 0:
            raise ValueError("max_size and acquire_timeout must be positive")
        self._factory, self._close = factory, close
        self._max_size, self._acquire_timeout = max_size, acquire_timeout
        self._entries: list[_Entry] = []
        self._condition = asyncio.Condition()
        self._closed = False
        self._creating = 0

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[Any]:
        entry = await self._take()
        try:
            yield entry.session
        finally:
            async with self._condition:
                entry.in_use = False
                self._condition.notify()

    async def _take(self) -> _Entry:
        async def wait_for_slot() -> _Entry:
            async with self._condition:
                while True:
                    if self._closed:
                        raise RuntimeError("session pool is closed")
                    for entry in self._entries:
                        if not entry.in_use:
                            entry.in_use = True
                            return entry
                    if len(self._entries) + self._creating < self._max_size:
                        self._creating += 1
                        break
                    await self._condition.wait()
            try:
                session = await self._factory()
            except BaseException:
                async with self._condition:
                    self._creating -= 1
                    self._condition.notify_all()
                raise
            async with self._condition:
                self._creating -= 1
                if self._closed:
                    await self._close(session)
                    self._condition.notify_all()
                    raise RuntimeError("session pool closed during connection")
                entry = _Entry(session=session, in_use=True)
                self._entries.append(entry)
                self._condition.notify_all()
                return entry

        return await asyncio.wait_for(wait_for_slot(), timeout=self._acquire_timeout)

    async def close(self) -> None:
        async with self._condition:
            self._closed = True
            while any(entry.in_use for entry in self._entries) or self._creating:
                self._condition.notify_all()
                await self._condition.wait()
            entries, self._entries = self._entries, []
        results = await asyncio.gather(
            *(self._close(entry.session) for entry in entries),
            return_exceptions=True,
        )
        failures = [result for result in results if isinstance(result, BaseException)]
        if failures:
            raise ExceptionGroup("one or more MCP sessions failed to close", failures)

    async def __aenter__(self) -> "SessionPool":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

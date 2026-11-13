"""Protocol-level health inspection for an initialized MCP session."""
from __future__ import annotations

import asyncio
import time
from dataclasses import asdict, dataclass
from typing import Any, Protocol


class HealthSession(Protocol):
    async def ping(self) -> Any: ...
    @property
    def _server_info(self) -> Any: ...


@dataclass(frozen=True, slots=True)
class HealthReport:
    status: str
    duration_ms: int
    server_name: str | None
    error_category: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


async def inspect_session(session: HealthSession, *, timeout_seconds: float = 3.0) -> HealthReport:
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    started = time.monotonic()
    try:
        await asyncio.wait_for(session.ping(), timeout=timeout_seconds)
        info = getattr(session, "_server_info", None)
        name = getattr(info, "name", None)
        return HealthReport(
            status="healthy",
            duration_ms=max(0, int((time.monotonic() - started) * 1000)),
            server_name=name if isinstance(name, str) else None,
        )
    except asyncio.TimeoutError:
        category = "timeout"
    except Exception:
        category = "protocol_or_connection_error"
    return HealthReport(
        status="unhealthy",
        duration_ms=max(0, int((time.monotonic() - started) * 1000)),
        server_name=None,
        error_category=category,
    )

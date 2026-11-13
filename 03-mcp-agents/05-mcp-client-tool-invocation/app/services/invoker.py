"""Policy and reliability boundary for MCP tool calls."""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Callable, Protocol


class CallToolSession(Protocol):
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any: ...


class ToolInvocationError(RuntimeError):
    pass


class ToolNotAllowed(ToolInvocationError):
    pass


class ToolCallTimedOut(ToolInvocationError):
    pass


@dataclass(frozen=True, slots=True)
class AuditEvent:
    tool_name: str
    correlation_id: str
    outcome: str
    duration_ms: int


class ToolInvoker:
    def __init__(
        self,
        session: CallToolSession,
        allowed_tools: set[str],
        *,
        timeout_seconds: float = 10.0,
        audit: Callable[[AuditEvent], None] | None = None,
    ) -> None:
        if not allowed_tools:
            raise ValueError("allowed_tools cannot be empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._session = session
        self._allowed = frozenset(allowed_tools)
        self._timeout = timeout_seconds
        self._audit = audit or (lambda _event: None)

    async def invoke(
        self, name: str, arguments: dict[str, Any], *, correlation_id: str = "local"
    ) -> Any:
        if name not in self._allowed:
            raise ToolNotAllowed(f"tool is not allowlisted: {name}")
        if not isinstance(arguments, dict):
            raise TypeError("tool arguments must be a JSON object")
        started = time.monotonic()
        outcome = "error"
        try:
            result = await asyncio.wait_for(
                self._session.call_tool(name, arguments), timeout=self._timeout
            )
            outcome = "success"
            return result
        except asyncio.TimeoutError as exc:
            outcome = "timeout"
            raise ToolCallTimedOut(f"tool call exceeded {self._timeout:g}s") from exc
        finally:
            event = AuditEvent(
                tool_name=name,
                correlation_id=correlation_id,
                outcome=outcome,
                duration_ms=max(0, int((time.monotonic() - started) * 1000)),
            )
            try:
                self._audit(event)
            except Exception:
                # Audit sink failures must be surfaced: silently losing audit records
                # would falsely imply that the call was fully observed.
                raise

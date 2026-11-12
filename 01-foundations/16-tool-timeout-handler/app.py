"""Backward-compatible facade; use tool_timeout for new code."""
from tool_timeout import (
    RequestDeadlineExceeded,
    ToolTimedOut,
    TimeoutResult,
    execute_with_timeout,
)

__all__ = [
    "RequestDeadlineExceeded",
    "ToolTimedOut",
    "TimeoutResult",
    "execute_with_timeout",
]

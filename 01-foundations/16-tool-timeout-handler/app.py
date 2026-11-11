"""Backward-compatible facade; use tool_timeout for new code."""
from tool_timeout import ToolTimedOut,TimeoutResult,execute_with_timeout
__all__=["ToolTimedOut","TimeoutResult","execute_with_timeout"]

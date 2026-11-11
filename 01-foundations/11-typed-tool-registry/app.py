"""Backward-compatible facade. New code should import from tool_registry."""
from tool_registry import ToolExecutionError, ToolRegistrationError, ToolRegistry, ToolSpec

__all__ = ["ToolExecutionError", "ToolRegistrationError", "ToolRegistry", "ToolSpec"]

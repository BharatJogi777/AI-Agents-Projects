"""Backward-compatible public imports; implementation lives in calculator_core."""

from calculator_core import (
    AgentStepLimitError,
    CalculationError,
    CalculatorAgent,
    TOOL_DEFINITIONS,
    calculate,
    execute_tool,
)
from calculator_core.provider import OllamaChatClient

__all__ = [
    "AgentStepLimitError",
    "CalculationError",
    "CalculatorAgent",
    "OllamaChatClient",
    "TOOL_DEFINITIONS",
    "calculate",
    "execute_tool",
]

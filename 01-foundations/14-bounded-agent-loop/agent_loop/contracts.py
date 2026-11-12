from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class AgentLoopError(RuntimeError):
    """Base class for bounded-loop termination and contract failures."""


class AgentStepLimitExceeded(AgentLoopError):
    """The agent consumed its complete iteration budget without finishing."""


class AgentToolLimitExceeded(AgentLoopError):
    """A step attempted to exceed the total or per-step tool-call budget."""


class AgentErrorLimitExceeded(AgentLoopError):
    """The cumulative error budget was exhausted."""


@dataclass(frozen=True, slots=True)
class LoopConfig:
    max_steps: int = 8
    max_tool_calls: int = 12
    max_tool_calls_per_step: int = 4
    max_consecutive_errors: int = 3
    max_total_errors: int = 8

    def __post_init__(self) -> None:
        ranges = {
            "max_steps": (1, 100),
            "max_tool_calls": (0, 500),
            "max_tool_calls_per_step": (0, 100),
            "max_consecutive_errors": (1, 20),
            "max_total_errors": (1, 100),
        }
        for name, (minimum, maximum) in ranges.items():
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
            if not minimum <= value <= maximum:
                raise ValueError(f"{name} must be {minimum}..{maximum}")


@dataclass(frozen=True, slots=True)
class StepResult:
    """Outcome of one iteration; counters describe this iteration only."""

    final: bool = False
    tool_calls: int = 0
    errors: int = 0
    value: Any = None

    def __post_init__(self) -> None:
        if type(self.final) is not bool:
            raise TypeError("final must be a boolean")
        for name in ("tool_calls", "errors"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be an integer")
            if value < 0:
                raise ValueError(f"{name} cannot be negative")


@dataclass(frozen=True, slots=True)
class StepSummary:
    index: int
    tool_calls: int
    errors: int
    final: bool


@dataclass(frozen=True, slots=True)
class LoopReport:
    value: Any
    steps: int
    tool_calls: int
    errors: int
    consecutive_errors: int
    stopped_reason: str
    history: tuple[StepSummary, ...] = ()

"""Public circuit-breaker value types."""
from dataclasses import dataclass
from enum import Enum


class CircuitOpen(RuntimeError):
    """Raised when a dependency call is rejected by an open circuit."""


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass(frozen=True, slots=True)
class CircuitSnapshot:
    state: CircuitState
    failures: int
    retry_at: float | None


@dataclass(frozen=True, slots=True)
class _Permit:
    generation: int
    probe: bool = False

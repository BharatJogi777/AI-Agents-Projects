"""Immutable retry policy and typed exhaustion error."""
from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Hard-bounded retry schedule. max_attempts includes the first call."""

    max_attempts: int = 3
    base_delay: float = 0.1
    max_delay: float = 2.0
    multiplier: float = 2.0
    jitter_ratio: float = 0.2
    max_elapsed: float | None = None

    def __post_init__(self) -> None:
        if type(self.max_attempts) is not int or not 1 <= self.max_attempts <= 10:
            raise ValueError("max_attempts must be an integer in [1, 10]")
        for name in ("base_delay", "max_delay", "multiplier", "jitter_ratio"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite number")
        if self.base_delay < 0 or self.max_delay < self.base_delay or self.max_delay > 300:
            raise ValueError("delays must satisfy 0 <= base_delay <= max_delay <= 300")
        if self.multiplier < 1 or self.multiplier > 10:
            raise ValueError("multiplier must be in [1, 10]")
        if not 0 <= self.jitter_ratio <= 1:
            raise ValueError("jitter_ratio must be in [0, 1]")
        if self.max_elapsed is not None:
            if isinstance(self.max_elapsed, bool) or not isinstance(self.max_elapsed, (int, float)):
                raise ValueError("max_elapsed must be a finite positive number")
            if not math.isfinite(self.max_elapsed) or not 0 < self.max_elapsed <= 3600:
                raise ValueError("max_elapsed must be in (0, 3600]")


class RetryExhausted(RuntimeError):
    """Raised when the configured retry budget is consumed."""

    def __init__(self, attempts: int, last_error: Exception, elapsed: float) -> None:
        super().__init__(f"operation failed after {attempts} attempt(s)")
        self.attempts = attempts
        self.last_error = last_error
        self.elapsed = elapsed

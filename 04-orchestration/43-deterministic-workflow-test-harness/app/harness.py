"""Small deterministic harness for testing workflow steps and retry policies."""
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class StepResult:
    value: Any = None
    attempts: int = 0
    error: Exception | None = None

class DeterministicHarness:
    def __init__(self, *, start_time: float = 0.0) -> None:
        self.now = start_time
        self.trace: list[tuple[str, float]] = []

    def advance(self, seconds: float) -> float:
        if seconds < 0:
            raise ValueError("time cannot move backwards")
        self.now += seconds
        return self.now

    def run_step(self, name: str, action: Callable[[], Any], *, max_attempts: int = 1,
                 retry_delay: float = 0.0) -> StepResult:
        if not name.strip() or max_attempts < 1 or retry_delay < 0:
            raise ValueError("invalid step name, attempts, or retry delay")
        result = StepResult()
        for attempt in range(1, max_attempts + 1):
            result.attempts = attempt
            self.trace.append((name, self.now))
            try:
                result.value = action()
                result.error = None
                return result
            except Exception as exc:
                result.error = exc
                if attempt < max_attempts:
                    self.advance(retry_delay)
        return result

    def assert_trace(self, expected: list[tuple[str, float]]) -> None:
        if self.trace != expected:
            raise AssertionError(f"trace mismatch: expected {expected!r}, got {self.trace!r}")

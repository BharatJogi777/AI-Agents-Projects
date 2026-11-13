from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from threading import Lock
from time import perf_counter
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class LatencySummary:
    tool: str
    count: int
    minimum_ms: float
    maximum_ms: float
    mean_ms: float
    p95_ms: float
    slow_calls: int


class LatencyMonitor:
    def __init__(self, *, sample_limit: int = 1000, slow_threshold_ms: float = 500.0):
        if sample_limit < 1:
            raise ValueError("sample_limit must be positive")
        if slow_threshold_ms < 0:
            raise ValueError("slow_threshold_ms cannot be negative")
        self._samples: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=sample_limit))
        self._slow: dict[str, int] = defaultdict(int)
        self._threshold = slow_threshold_ms
        self._lock = Lock()

    def observe(self, tool: str, duration_ms: float) -> None:
        if not tool or not tool.strip():
            raise ValueError("tool name is required")
        if duration_ms < 0:
            raise ValueError("duration cannot be negative")
        with self._lock:
            self._samples[tool].append(float(duration_ms))
            if duration_ms >= self._threshold:
                self._slow[tool] += 1

    def measure(self, tool: str, operation: Callable[[], T]) -> T:
        started = perf_counter()
        try:
            return operation()
        finally:
            self.observe(tool, (perf_counter() - started) * 1000)

    def summary(self, tool: str) -> LatencySummary:
        with self._lock:
            values = sorted(self._samples.get(tool, ()))
            slow = self._slow.get(tool, 0)
        if not values:
            raise KeyError(f"no samples for tool: {tool}")
        rank = max(0, min(len(values) - 1, int((0.95 * len(values) + 0.999999)) - 1))
        return LatencySummary(tool, len(values), values[0], values[-1],
                              sum(values) / len(values), values[rank], slow)

    def tools(self) -> list[str]:
        with self._lock:
            return sorted(self._samples)

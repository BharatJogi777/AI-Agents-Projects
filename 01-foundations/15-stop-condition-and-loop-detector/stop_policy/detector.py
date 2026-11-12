"""Bounded, thread-safe repeated-state detection."""
from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from threading import RLock
from typing import Any

from .fingerprint import fingerprint_state


@dataclass(frozen=True, slots=True)
class StopDecision:
    stop: bool
    reason: str


class LoopDetector:
    """Detect repeated snapshots in a rolling window.

    max_repeats counts occurrences *after the first occurrence*. With
    max_repeats=2, the third observation of the same state triggers a stop.
    The window is bounded, so old states eventually age out.
    """

    def __init__(
        self,
        max_repeats: int = 2,
        history_size: int = 20,
        *,
        max_state_bytes: int = 64_000,
    ) -> None:
        if type(max_repeats) is not int or not 1 <= max_repeats <= 100:
            raise ValueError("max_repeats must be an integer in 1..100")
        if type(history_size) is not int or not max_repeats + 1 <= history_size <= 10_000:
            raise ValueError("history_size must be max_repeats+1..10000")
        if type(max_state_bytes) is not int or not 128 <= max_state_bytes <= 1_000_000:
            raise ValueError("max_state_bytes must be an integer in 128..1000000")

        self.max_repeats = max_repeats
        self._recent: deque[str] = deque()
        self._counts: Counter[str] = Counter()
        self._history_size = history_size
        self._max_state_bytes = max_state_bytes
        self._lock = RLock()

    @staticmethod
    def fingerprint(state: Any) -> str:
        return fingerprint_state(state)

    @property
    def history_size(self) -> int:
        with self._lock:
            return len(self._recent)

    def observe(self, state: Any) -> StopDecision:
        key = fingerprint_state(state, max_bytes=self._max_state_bytes)
        with self._lock:
            previous_occurrences = self._counts[key]
            self._recent.append(key)
            self._counts[key] += 1

            if len(self._recent) > self._history_size:
                expired = self._recent.popleft()
                self._counts[expired] -= 1
                if self._counts[expired] == 0:
                    del self._counts[expired]

            repeated_occurrences = previous_occurrences
            should_stop = repeated_occurrences >= self.max_repeats
        return StopDecision(should_stop, "repeated_state" if should_stop else "continue")

    def reset(self) -> None:
        """Clear history between independent agent runs."""
        with self._lock:
            self._recent.clear()
            self._counts.clear()

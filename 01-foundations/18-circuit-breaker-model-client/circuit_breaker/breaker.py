"""Thread-safe, process-local circuit breaker."""
from __future__ import annotations

import math
import threading
import time
from collections.abc import Callable
from typing import Any

from .contracts import CircuitOpen, CircuitSnapshot, CircuitState, _Permit


class CircuitBreaker:
    """Protect a dependency with CLOSED/OPEN/HALF_OPEN state transitions.

    The operation runs outside the lock. A generation token prevents a late
    completion from an older in-flight request from mutating a newer circuit.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_seconds: float = 10.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if type(failure_threshold) is not int or not 1 <= failure_threshold <= 1000:
            raise ValueError("failure_threshold must be an integer in [1, 1000]")
        if isinstance(recovery_seconds, bool) or not isinstance(recovery_seconds, (int, float)):
            raise ValueError("recovery_seconds must be a finite number")
        if not math.isfinite(recovery_seconds) or not 0 < recovery_seconds <= 3600:
            raise ValueError("recovery_seconds must be in (0, 3600]")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self.threshold = failure_threshold
        self.recovery_seconds = float(recovery_seconds)
        self.clock = clock
        self._state = CircuitState.CLOSED
        self._failures = 0
        self._opened_at: float | None = None
        self._probe_in_flight = False
        self._generation = 0
        self._lock = threading.Lock()

    def _now(self) -> float:
        value = self.clock()
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("clock must return a finite monotonic timestamp")
        return float(value)

    def _acquire(self) -> _Permit:
        with self._lock:
            now = self._now()
            if self._state is CircuitState.OPEN:
                if self._opened_at is None or now - self._opened_at < self.recovery_seconds:
                    raise CircuitOpen("circuit is open")
                self._state = CircuitState.HALF_OPEN

            if self._state is CircuitState.HALF_OPEN:
                if self._probe_in_flight:
                    raise CircuitOpen("half-open recovery probe is already in flight")
                self._probe_in_flight = True
                return _Permit(self._generation, True)

            return _Permit(self._generation, False)

    def _success(self, permit: _Permit) -> None:
        with self._lock:
            if permit.generation != self._generation:
                return
            if self._state is CircuitState.OPEN:
                return
            self._state = CircuitState.CLOSED
            self._failures = 0
            self._opened_at = None
            self._probe_in_flight = False
            self._generation += 1

    def _failure(self, permit: _Permit) -> None:
        with self._lock:
            if permit.generation != self._generation or self._state is CircuitState.OPEN:
                return
            self._probe_in_flight = False
            self._failures += 1
            if self._state is CircuitState.HALF_OPEN or self._failures >= self.threshold:
                self._state = CircuitState.OPEN
                self._opened_at = self._now()
                self._generation += 1

    def _abandon(self, permit: _Permit) -> None:
        """Release a half-open probe if caller cancellation aborts the operation."""
        if not permit.probe:
            return
        with self._lock:
            if permit.generation == self._generation and self._state is CircuitState.HALF_OPEN:
                self._probe_in_flight = False

    def call(self, operation: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute operation if permitted; record ordinary exceptions as failures."""
        if not callable(operation):
            raise TypeError("operation must be callable")
        permit = self._acquire()
        try:
            result = operation(*args, **kwargs)
        except Exception:
            self._failure(permit)
            raise
        except BaseException:
            # Cancellation/interrupt is not a dependency failure, but must not
            # permanently occupy the single HALF_OPEN probe slot.
            self._abandon(permit)
            raise
        self._success(permit)
        return result

    def snapshot(self) -> CircuitSnapshot:
        """Return an immutable, internally consistent state snapshot."""
        with self._lock:
            retry_at = self._opened_at + self.recovery_seconds if self._opened_at is not None else None
            return CircuitSnapshot(self._state, self._failures, retry_at)

    # Compatibility methods for manually managed calls. Prefer call(), which
    # associates completions with generation tokens and handles cancellation.
    def before_call(self) -> None:
        self._legacy_permit = self._acquire()

    def record_success(self) -> None:
        permit = getattr(self, "_legacy_permit", None)
        if permit is not None:
            self._success(permit)
            self._legacy_permit = None

    def record_failure(self) -> None:
        permit = getattr(self, "_legacy_permit", None)
        if permit is not None:
            self._failure(permit)
            self._legacy_permit = None

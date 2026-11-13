"""Synchronous, bounded retry execution."""
from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import TypeVar

from .policy import RetryExhausted, RetryPolicy

T = TypeVar("T")
# Deliberately narrow defaults: callers can supply a provider-specific classifier.
_DEFAULT_RETRYABLE = (ConnectionError, TimeoutError)


def retry(
    operation: Callable[[], T],
    policy: RetryPolicy | None = None,
    *,
    idempotent: bool = False,
    retry_if: Callable[[Exception], bool] | None = None,
    retry_after: Callable[[Exception], float | None] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    random_value: Callable[[], float] = random.random,
    clock: Callable[[], float] = time.monotonic,
) -> T:
    """Run an operation with bounded retries.

    The first attempt always runs. Further attempts require idempotent=True.
    retry_if defaults to ConnectionError/TimeoutError; custom classifiers should
    be narrow and must not raise. retry_after may return a server delay in seconds.
    """
    if not callable(operation) or not callable(sleep) or not callable(random_value) or not callable(clock):
        raise TypeError("operation, sleep, random_value and clock must be callable")
    if retry_if is not None and not callable(retry_if):
        raise TypeError("retry_if must be callable")
    if retry_after is not None and not callable(retry_after):
        raise TypeError("retry_after must be callable")
    if type(idempotent) is not bool:
        raise TypeError("idempotent must be a bool")

    policy = policy or RetryPolicy()
    started = clock()
    if not isinstance(started, (int, float)) or not started >= 0:
        raise ValueError("clock must return a non-negative monotonic value")

    for attempt in range(1, policy.max_attempts + 1):
        try:
            return operation()
        except Exception as exc:
            elapsed = max(0.0, clock() - started)
            classifier = retry_if or (lambda error: isinstance(error, _DEFAULT_RETRYABLE))
            if not idempotent or not classifier(exc):
                raise
            if attempt >= policy.max_attempts:
                raise RetryExhausted(attempt, exc, elapsed) from exc

            ceiling = min(policy.max_delay, policy.base_delay * (policy.multiplier ** (attempt - 1)))
            sample = random_value()
            if isinstance(sample, bool) or not isinstance(sample, (int, float)) or not 0 <= sample <= 1:
                raise ValueError("random_value must return a number in [0, 1]")
            delay = ceiling * (1 + policy.jitter_ratio * (2 * sample - 1))

            if retry_after is not None:
                server_delay = retry_after(exc)
                if server_delay is not None:
                    if isinstance(server_delay, bool) or not isinstance(server_delay, (int, float)):
                        raise ValueError("retry_after must return a finite number or None")
                    if server_delay < 0 or server_delay != server_delay or server_delay == float("inf"):
                        raise ValueError("retry_after must return a finite non-negative number")
                    delay = max(delay, float(server_delay))
            delay = min(policy.max_delay, max(0.0, delay))

            if policy.max_elapsed is not None:
                remaining = policy.max_elapsed - max(0.0, clock() - started)
                if remaining <= 0:
                    raise RetryExhausted(attempt, exc, max(0.0, clock() - started)) from exc
                if delay >= remaining:
                    raise RetryExhausted(attempt, exc, max(0.0, clock() - started)) from exc
            if delay:
                sleep(delay)

    raise AssertionError("unreachable")

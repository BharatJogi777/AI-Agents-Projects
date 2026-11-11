"""Bounded retry helpers with exponential backoff, jitter, and injectable timing."""
import random
import time
from dataclasses import dataclass
from typing import Callable, TypeVar

T=TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts:int=3
    base_delay:float=0.1
    max_delay:float=2.0
    jitter_ratio:float=0.2

    def __post_init__(self):
        if not 1<=self.max_attempts<=10: raise ValueError("max_attempts must be 1..10")
        if self.base_delay<0 or self.max_delay<self.base_delay: raise ValueError("invalid delay bounds")
        if not 0<=self.jitter_ratio<=1: raise ValueError("jitter_ratio must be 0..1")


class RetryExhausted(RuntimeError):
    def __init__(self,attempts:int,last_error:Exception):
        super().__init__(f"operation failed after {attempts} attempts")
        self.attempts=attempts
        self.last_error=last_error


def retry(operation:Callable[[],T],policy:RetryPolicy=RetryPolicy(),*,
          retry_if:Callable[[Exception],bool]|None=None,
          sleep:Callable[[float],None]=time.sleep,
          random_value:Callable[[],float]=random.random)->T:
    for attempt in range(1,policy.max_attempts+1):
        try: return operation()
        except Exception as exc:
            if retry_if is not None and not retry_if(exc): raise
            if attempt==policy.max_attempts: raise RetryExhausted(attempt,exc) from exc
            ceiling=min(policy.max_delay,policy.base_delay*(2**(attempt-1)))
            jitter=ceiling*policy.jitter_ratio*(2*random_value()-1)
            sleep(max(0.0,ceiling+jitter))
    raise AssertionError("unreachable")

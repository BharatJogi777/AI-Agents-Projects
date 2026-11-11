from dataclasses import dataclass

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts:int=3
    base_delay:float=0.1
    max_delay:float=2.0
    jitter_ratio:float=0.2
    def __post_init__(self):
        if type(self.max_attempts) is not int or not 1<=self.max_attempts<=10: raise ValueError("max_attempts must be 1..10")
        if self.base_delay<0 or self.max_delay<self.base_delay or self.max_delay>300: raise ValueError("invalid delay bounds")
        if not 0<=self.jitter_ratio<=1: raise ValueError("jitter_ratio must be 0..1")

class RetryExhausted(RuntimeError):
    def __init__(self,attempts:int,last_error:Exception):
        super().__init__(f"operation failed after {attempts} attempts")
        self.attempts=attempts; self.last_error=last_error

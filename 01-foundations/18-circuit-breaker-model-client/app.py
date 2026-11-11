"""Thread-safe circuit breaker for protecting an unreliable model/provider client."""
import threading
import time
from dataclasses import dataclass
from enum import Enum


class CircuitOpen(RuntimeError): pass
class CircuitState(str,Enum):
    CLOSED="closed"
    OPEN="open"
    HALF_OPEN="half_open"


@dataclass(frozen=True)
class CircuitSnapshot:
    state:CircuitState
    failures:int
    retry_at:float|None


class CircuitBreaker:
    def __init__(self,failure_threshold:int=3,recovery_seconds:float=10.0,
                 clock=time.monotonic):
        if failure_threshold<1 or recovery_seconds<=0: raise ValueError("invalid breaker configuration")
        self.threshold,self.recovery_seconds,self.clock=failure_threshold,recovery_seconds,clock
        self._state=CircuitState.CLOSED
        self._failures=0
        self._opened_at:float|None=None
        self._probe_in_flight=False
        self._lock=threading.Lock()

    def before_call(self):
        with self._lock:
            now=self.clock()
            if self._state is CircuitState.OPEN:
                if self._opened_at is None or now-self._opened_at<self.recovery_seconds:
                    raise CircuitOpen("circuit is open")
                self._state=CircuitState.HALF_OPEN
            if self._state is CircuitState.HALF_OPEN:
                if self._probe_in_flight: raise CircuitOpen("half-open probe already in flight")
                self._probe_in_flight=True

    def record_success(self):
        with self._lock:
            self._state=CircuitState.CLOSED
            self._failures=0
            self._opened_at=None
            self._probe_in_flight=False

    def record_failure(self):
        with self._lock:
            self._probe_in_flight=False
            self._failures+=1
            if self._state is CircuitState.HALF_OPEN or self._failures>=self.threshold:
                self._state=CircuitState.OPEN
                self._opened_at=self.clock()

    def snapshot(self):
        with self._lock:
            retry_at=(self._opened_at+self.recovery_seconds) if self._opened_at is not None else None
            return CircuitSnapshot(self._state,self._failures,retry_at)

    def call(self,operation,*args,**kwargs):
        self.before_call()
        try: result=operation(*args,**kwargs)
        except Exception:
            self.record_failure()
            raise
        self.record_success()
        return result

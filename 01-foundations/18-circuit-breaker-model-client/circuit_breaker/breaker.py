import threading,time
from typing import Callable,Any
from .contracts import CircuitOpen,CircuitSnapshot,CircuitState,_Permit

class CircuitBreaker:
    """Thread-safe breaker; late completions from older generations cannot close it."""
    def __init__(self,failure_threshold:int=3,recovery_seconds:float=10.0,clock:Callable[[],float]=time.monotonic):
        if type(failure_threshold) is not int or failure_threshold<1 or not 0<recovery_seconds<=3600: raise ValueError("invalid breaker configuration")
        self.threshold,self.recovery_seconds,self.clock=failure_threshold,recovery_seconds,clock
        self._state=CircuitState.CLOSED; self._failures=0; self._opened_at=None
        self._probe_in_flight=False; self._generation=0; self._lock=threading.Lock()
    def _acquire(self)->_Permit:
        with self._lock:
            now=self.clock()
            if self._state is CircuitState.OPEN:
                if self._opened_at is None or now-self._opened_at<self.recovery_seconds: raise CircuitOpen("circuit is open")
                self._state=CircuitState.HALF_OPEN
            if self._state is CircuitState.HALF_OPEN:
                if self._probe_in_flight: raise CircuitOpen("half-open probe already in flight")
                self._probe_in_flight=True
                return _Permit(self._generation,True)
            return _Permit(self._generation,False)
    def before_call(self)->None:
        # Compatibility API for callers that manually pair before_call with record_*.
        self._acquire_legacy()
    def _acquire_legacy(self)->None:
        with self._lock:
            now=self.clock()
            if self._state is CircuitState.OPEN:
                if self._opened_at is None or now-self._opened_at<self.recovery_seconds: raise CircuitOpen("circuit is open")
                self._state=CircuitState.HALF_OPEN
            if self._state is CircuitState.HALF_OPEN:
                if self._probe_in_flight: raise CircuitOpen("half-open probe already in flight")
                self._probe_in_flight=True
    def _success(self,permit:_Permit|None)->None:
        with self._lock:
            if permit is not None and permit.generation!=self._generation: return
            if self._state is CircuitState.OPEN and permit is not None: return
            self._state=CircuitState.CLOSED; self._failures=0; self._opened_at=None; self._probe_in_flight=False
            self._generation+=1
    def record_success(self)->None: self._success(None)
    def _failure(self,permit:_Permit|None)->None:
        with self._lock:
            if permit is not None and permit.generation!=self._generation: return
            if self._state is CircuitState.OPEN and permit is not None: return
            self._probe_in_flight=False; self._failures+=1
            if self._state is CircuitState.HALF_OPEN or self._failures>=self.threshold:
                self._state=CircuitState.OPEN; self._opened_at=self.clock(); self._generation+=1
    def record_failure(self)->None: self._failure(None)
    def snapshot(self)->CircuitSnapshot:
        with self._lock:
            retry_at=self._opened_at+self.recovery_seconds if self._opened_at is not None else None
            return CircuitSnapshot(self._state,self._failures,retry_at)
    def call(self,operation:Callable[...,Any],*args,**kwargs):
        permit=self._acquire()
        try: result=operation(*args,**kwargs)
        except Exception:
            self._failure(permit); raise
        self._success(permit); return result

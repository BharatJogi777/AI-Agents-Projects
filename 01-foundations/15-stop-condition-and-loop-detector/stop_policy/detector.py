from collections import deque
from dataclasses import dataclass
from threading import Lock
from typing import Any
from .fingerprint import fingerprint_state
@dataclass(frozen=True)
class StopDecision:
    stop:bool
    reason:str
class LoopDetector:
    def __init__(self,max_repeats:int=2,history_size:int=20):
        if max_repeats<1 or history_size<max_repeats: raise ValueError("history_size must be >= max_repeats >= 1")
        self.max_repeats=max_repeats; self.history_size=history_size
        self._recent=deque(maxlen=history_size); self._lock=Lock()
    @staticmethod
    def fingerprint(state:Any)->str: return fingerprint_state(state)
    def observe(self,state:Any)->StopDecision:
        key=self.fingerprint(state)
        with self._lock:
            repeats=self._recent.count(key); self._recent.append(key)
        return StopDecision(repeats>=self.max_repeats,"repeated_state" if repeats>=self.max_repeats else "continue")

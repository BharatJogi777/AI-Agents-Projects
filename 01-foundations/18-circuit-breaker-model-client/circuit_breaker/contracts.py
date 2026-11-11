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

@dataclass(frozen=True)
class _Permit:
    generation:int
    probe:bool=False

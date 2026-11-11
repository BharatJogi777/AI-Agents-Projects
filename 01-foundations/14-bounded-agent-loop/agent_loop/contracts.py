from dataclasses import dataclass
from typing import Any

class AgentStepLimitExceeded(RuntimeError): pass
class AgentToolLimitExceeded(RuntimeError): pass

@dataclass(frozen=True)
class LoopConfig:
    max_steps:int=8
    max_tool_calls:int=12
    max_consecutive_errors:int=3
    def __post_init__(self):
        if not 1<=self.max_steps<=100: raise ValueError("max_steps must be 1..100")
        if not 0<=self.max_tool_calls<=500: raise ValueError("max_tool_calls must be 0..500")
        if not 1<=self.max_consecutive_errors<=20: raise ValueError("max_consecutive_errors must be 1..20")

@dataclass(frozen=True)
class StepResult:
    final:bool=False
    tool_calls:int=0
    errors:int=0
    value:Any=None

@dataclass(frozen=True)
class LoopReport:
    value:Any
    steps:int
    tool_calls:int
    errors:int
    stopped_reason:str

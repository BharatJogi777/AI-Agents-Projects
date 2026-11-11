"""Framework-independent controller for a bounded agent execution loop."""
from dataclasses import dataclass
from typing import Any, Callable


class AgentStepLimitExceeded(RuntimeError): pass
class AgentToolLimitExceeded(RuntimeError): pass


@dataclass(frozen=True)
class LoopConfig:
    max_steps: int = 8
    max_tool_calls: int = 12
    max_consecutive_errors: int = 3

    def __post_init__(self):
        if not 1 <= self.max_steps <= 100: raise ValueError("max_steps must be 1..100")
        if not 0 <= self.max_tool_calls <= 500: raise ValueError("max_tool_calls must be 0..500")
        if not 1 <= self.max_consecutive_errors <= 20: raise ValueError("max_consecutive_errors must be 1..20")


@dataclass(frozen=True)
class StepResult:
    final: bool = False
    tool_calls: int = 0
    errors: int = 0
    value: Any = None


@dataclass(frozen=True)
class LoopReport:
    value: Any
    steps: int
    tool_calls: int
    errors: int
    stopped_reason: str


def run_bounded_loop(step: Callable[[int], StepResult], config: LoopConfig = LoopConfig()) -> LoopReport:
    tool_calls = errors = consecutive_errors = 0
    last_value = None
    for index in range(1, config.max_steps + 1):
        result = step(index)
        if not isinstance(result, StepResult): raise TypeError("step callback must return StepResult")
        if result.tool_calls < 0 or result.errors < 0: raise ValueError("counters cannot be negative")
        if tool_calls + result.tool_calls > config.max_tool_calls:
            raise AgentToolLimitExceeded("tool-call budget exceeded")
        tool_calls += result.tool_calls
        errors += result.errors
        consecutive_errors = consecutive_errors + result.errors if result.errors else 0
        last_value = result.value
        if consecutive_errors >= config.max_consecutive_errors:
            return LoopReport(last_value,index,tool_calls,errors,"consecutive_error_limit")
        if result.final:
            return LoopReport(last_value,index,tool_calls,errors,"final_answer")
    raise AgentStepLimitExceeded(f"agent exceeded {config.max_steps} steps")

from typing import Callable
from .contracts import AgentStepLimitExceeded,AgentToolLimitExceeded,LoopConfig,LoopReport,StepResult

def run_bounded_loop(step:Callable[[int],StepResult],config:LoopConfig|None=None)->LoopReport:
    """Execute injected agent iterations under independent budgets."""
    config=config or LoopConfig(); calls=errors=consecutive=0; last=None
    for index in range(1,config.max_steps+1):
        result=step(index)
        if not isinstance(result,StepResult): raise TypeError("step callback must return StepResult")
        if type(result.tool_calls) is not int or type(result.errors) is not int: raise TypeError("step counters must be integers")
        if result.tool_calls<0 or result.errors<0: raise ValueError("step counters cannot be negative")
        if calls+result.tool_calls>config.max_tool_calls: raise AgentToolLimitExceeded("tool-call budget exceeded")
        calls+=result.tool_calls; errors+=result.errors
        consecutive=consecutive+result.errors if result.errors else 0; last=result.value
        if consecutive>=config.max_consecutive_errors: return LoopReport(last,index,calls,errors,"consecutive_error_limit")
        if result.final: return LoopReport(last,index,calls,errors,"final_answer")
    raise AgentStepLimitExceeded(f"agent exceeded {config.max_steps} steps")

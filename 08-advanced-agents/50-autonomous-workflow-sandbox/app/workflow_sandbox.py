"""Execute only registered pure workflow steps with bounded state and trace output."""
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Step:
    name: str
    input_key: str
    output_key: str

@dataclass(frozen=True)
class Trace:
    step: str
    status: str
    output_key: str

def run_sandbox(initial_state: dict[str,Any], steps: list[Step], *, registry: dict[str,Callable[[Any],Any]], max_steps: int=20) -> tuple[dict[str,Any],list[Trace]]:
    if len(steps)>max_steps or max_steps<1:
        raise ValueError("workflow exceeds step limit")
    state=dict(initial_state)
    trace=[]
    for step in steps:
        if step.name not in registry:
            raise ValueError(f"unregistered step: {step.name}")
        if step.input_key not in state:
            raise KeyError(step.input_key)
        result=registry[step.name](state[step.input_key])
        state[step.output_key]=result
        trace.append(Trace(step.name,"completed",step.output_key))
    return state,trace

from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Step:
    name: str
    execute: Callable[[], Any]
    compensate: Callable[[], Any]

@dataclass(frozen=True)
class WorkflowResult:
    completed: tuple[str, ...]
    compensated: tuple[str, ...]
    error: str | None

class CompensationWorkflow:
    def __init__(self, steps: list[Step]):
        if not steps or len({s.name for s in steps}) != len(steps): raise ValueError("unique steps required")
        self.steps=tuple(steps)

    def run(self) -> WorkflowResult:
        done=[]
        try:
            for step in self.steps:
                step.execute(); done.append(step)
            return WorkflowResult(tuple(s.name for s in done),(),None)
        except Exception as exc:
            compensated=[]
            errors=[]
            for step in reversed(done):
                try: step.compensate(); compensated.append(step.name)
                except Exception as compensation_error: errors.append(f"{step.name}: {compensation_error}")
            message=str(exc)
            if errors: message += "; compensation errors: " + "; ".join(errors)
            return WorkflowResult(tuple(s.name for s in done),tuple(compensated),message)

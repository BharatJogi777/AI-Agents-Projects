from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class SagaStep:
    name: str
    action: Callable[[], Any]
    compensate: Callable[[], Any]

@dataclass(frozen=True)
class SagaRecord:
    status: str
    completed: tuple[str, ...]
    compensated: tuple[str, ...]
    outputs: dict[str, Any]
    failure: str | None = None

class Saga:
    def __init__(self, steps: list[SagaStep]):
        if not steps or len({s.name for s in steps}) != len(steps): raise ValueError("unique saga steps required")
        self.steps=tuple(steps)

    def execute(self) -> SagaRecord:
        completed=[]; outputs={}
        try:
            for step in self.steps:
                outputs[step.name]=step.action()
                completed.append(step)
            return SagaRecord("completed",tuple(s.name for s in completed),(),outputs)
        except Exception as exc:
            compensated=[]; errors=[]
            for step in reversed(completed):
                try: step.compensate(); compensated.append(step.name)
                except Exception as err: errors.append(f"{step.name}: {err}")
            status="compensated" if not errors else "compensation_failed"
            return SagaRecord(status,tuple(s.name for s in completed),tuple(compensated),outputs,str(exc),) if not errors else SagaRecord(status,tuple(s.name for s in completed),tuple(compensated),outputs,str(exc)+"; "+"; ".join(errors))

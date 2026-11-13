from dataclasses import dataclass, field
from typing import Any, Callable

Step = Callable[[dict[str, Any]], dict[str, Any]]

@dataclass
class WorkflowResult:
    state: dict[str, Any]
    completed: list[str] = field(default_factory=list)
    failed_step: str | None = None
    error: str | None = None

class SequentialWorkflow:
    def __init__(self, steps: list[tuple[str, Step]], *, max_retries: int = 0):
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        names = [name for name, _ in steps]
        if any(not name.strip() for name in names) or len(names) != len(set(names)):
            raise ValueError("step names must be non-empty and unique")
        self.steps, self.max_retries = tuple(steps), max_retries

    def run(self, initial: dict[str, Any]) -> WorkflowResult:
        state = dict(initial)
        result = WorkflowResult(state)
        for name, step in self.steps:
            for attempt in range(self.max_retries + 1):
                try:
                    update = step(dict(state))
                    if not isinstance(update, dict):
                        raise TypeError("workflow step must return a dictionary")
                    state.update(update)
                    result.state = dict(state)
                    result.completed.append(name)
                    break
                except Exception as exc:
                    if attempt == self.max_retries:
                        result.failed_step, result.error = name, str(exc)
                        result.state = state
                        return result
        return result

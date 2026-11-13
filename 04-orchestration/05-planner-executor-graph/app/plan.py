from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class PlanStep:
    id: str
    depends_on: tuple[str, ...] = ()

@dataclass(frozen=True)
class GraphResult:
    outputs: dict[str, Any]
    failures: dict[str, str]
    skipped: tuple[str, ...]

class PlannerExecutor:
    def __init__(self, handlers: dict[str, Callable[[dict[str, Any]], Any]], max_steps: int = 20):
        if max_steps < 1:
            raise ValueError("max_steps must be positive")
        self.handlers, self.max_steps = dict(handlers), max_steps

    def validate(self, plan: list[PlanStep]) -> None:
        if not plan or len(plan) > self.max_steps:
            raise ValueError("plan size outside configured bounds")
        ids = [step.id for step in plan]
        if any(not item.strip() for item in ids) or len(ids) != len(set(ids)):
            raise ValueError("step ids must be unique and non-empty")
        known, completed = set(ids), set()
        remaining = {step.id: set(step.depends_on) for step in plan}
        for step in plan:
            if not set(step.depends_on).issubset(known):
                raise ValueError(f"unknown dependency in {step.id}")
            if step.id in step.depends_on:
                raise ValueError("step cannot depend on itself")
        while remaining:
            ready = {key for key, deps in remaining.items() if deps.issubset(completed)}
            if not ready:
                raise ValueError("plan contains a dependency cycle")
            completed.update(ready)
            for key in ready:
                del remaining[key]

    def run(self, plan: list[PlanStep], context: dict[str, Any] | None = None) -> GraphResult:
        self.validate(plan)
        outputs, failures, skipped = {}, {}, []
        for step in plan:
            if any(dep in failures or dep in skipped for dep in step.depends_on):
                skipped.append(step.id)
                continue
            handler = self.handlers.get(step.id)
            if handler is None:
                failures[step.id] = "no handler registered"
                continue
            try:
                outputs[step.id] = handler({**(context or {}), **outputs})
            except Exception as exc:
                failures[step.id] = str(exc)
        return GraphResult(outputs, failures, tuple(skipped))

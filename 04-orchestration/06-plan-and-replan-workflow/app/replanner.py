from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Step:
    id: str
    run: Callable[[dict[str, Any]], dict[str, Any]]

@dataclass(frozen=True)
class ReplanResult:
    state: dict[str, Any]
    completed: tuple[str, ...]
    failed: str | None
    replans: int

class PlanAndReplan:
    def __init__(self, planner: Callable[[dict[str, Any], tuple[str, ...]], list[Step]], max_replans: int = 1, max_steps: int = 20):
        if max_replans < 0 or max_steps < 1: raise ValueError("invalid replan or step limit")
        self.planner, self.max_replans, self.max_steps = planner, max_replans, max_steps

    def run(self, initial: dict[str, Any]) -> ReplanResult:
        state, completed, replans = dict(initial), [], 0
        while True:
            steps = self.planner(dict(state), tuple(completed))
            if not isinstance(steps, list) or len(steps) > self.max_steps:
                raise ValueError("planner returned invalid or oversized plan")
            ids = [s.id for s in steps]
            if any(not x.strip() for x in ids) or len(ids) != len(set(ids)) or set(ids) & set(completed):
                raise ValueError("plan contains invalid or already completed step ids")
            failure = None
            for step in steps:
                try:
                    update = step.run(dict(state))
                    if not isinstance(update, dict): raise TypeError("step must return a dictionary")
                    state.update(update)
                    completed.append(step.id)
                except Exception:
                    failure = step.id
                    break
            if failure is None:
                return ReplanResult(state, tuple(completed), None, replans)
            if replans >= self.max_replans:
                return ReplanResult(state, tuple(completed), failure, replans)
            replans += 1

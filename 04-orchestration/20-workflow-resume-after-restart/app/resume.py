from dataclasses import dataclass
from typing import Callable, Any
from app.state_store import SQLiteStateStore

@dataclass(frozen=True)
class ResumeResult:
    workflow_id: str
    completed: tuple[str, ...]
    outputs: dict[str, Any]
    resumed: bool

class ResumableWorkflow:
    def __init__(self, store: SQLiteStateStore, steps: list[tuple[str, Callable[[dict[str, Any]], Any]]]):
        if not steps or len({n for n, _ in steps}) != len(steps):
            raise ValueError("steps must be non-empty and uniquely named")
        self.store, self.steps = store, tuple(steps)

    def run(self, workflow_id: str, initial: dict[str, Any] | None = None) -> ResumeResult:
        saved = self.store.load(workflow_id)
        resumed = saved is not None
        state = dict(saved.state if saved else (initial or {}))
        completed = list(state.get("_completed", []))
        expected = [name for name, _ in self.steps[:len(completed)]]
        if completed != expected: raise ValueError("persisted workflow progress does not match definition")
        version = saved.version if saved else 0
        for name, handler in self.steps[len(completed):]:
            value = handler(dict(state))
            state[name] = value
            completed.append(name)
            state["_completed"] = list(completed)
            stored = self.store.save(workflow_id, state, expected_version=version)
            version = stored.version
        return ResumeResult(workflow_id, tuple(completed), state, resumed)

from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Assignment:
    worker: str
    task: str

@dataclass(frozen=True)
class TeamResult:
    worker: str | None
    output: Any = None
    error: str | None = None

class SupervisorTeam:
    def __init__(self, workers: dict[str, Callable[[str], Any]], supervisor: Callable[[str, tuple[str, ...]], Assignment]):
        if not workers: raise ValueError("at least one worker is required")
        self.workers, self.supervisor = dict(workers), supervisor

    def run(self, task: str) -> TeamResult:
        if not task or not task.strip(): raise ValueError("task is required")
        assignment = self.supervisor(task, tuple(sorted(self.workers)))
        if not isinstance(assignment, Assignment) or not assignment.task.strip():
            raise ValueError("supervisor returned invalid assignment")
        worker = self.workers.get(assignment.worker)
        if worker is None: return TeamResult(None, error="supervisor selected an unknown worker")
        try:
            return TeamResult(assignment.worker, output=worker(assignment.task))
        except Exception as exc:
            return TeamResult(assignment.worker, error=str(exc))

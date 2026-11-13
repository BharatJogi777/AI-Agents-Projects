from dataclasses import dataclass
from enum import Enum
from time import time

class Status(str, Enum):
    QUEUED="queued"; RUNNING="running"; SUCCEEDED="succeeded"; FAILED="failed"; CANCELLED="cancelled"

@dataclass
class Task:
    task_id: str
    status: Status = Status.QUEUED
    attempts: int = 0
    lease_until: float = 0
    result: str | None = None
    error: str | None = None

class TaskCoordinator:
    def __init__(self, max_attempts: int = 3, lease_seconds: int = 60):
        if max_attempts < 1 or lease_seconds < 1: raise ValueError("positive limits required")
        self.max_attempts, self.lease_seconds = max_attempts, lease_seconds
        self.tasks: dict[str, Task] = {}

    def submit(self, task_id: str) -> Task:
        if not task_id.strip() or task_id in self.tasks: raise ValueError("task id must be unique and non-empty")
        self.tasks[task_id] = Task(task_id)
        return self.tasks[task_id]

    def claim(self, task_id: str, now: float | None = None) -> Task:
        task = self.tasks[task_id]; now = time() if now is None else now
        if task.status not in (Status.QUEUED, Status.FAILED) or task.attempts >= self.max_attempts:
            raise RuntimeError("task is not claimable")
        task.status, task.attempts = Status.RUNNING, task.attempts + 1
        task.lease_until = now + self.lease_seconds
        return task

    def heartbeat(self, task_id: str, now: float | None = None) -> None:
        task = self.tasks[task_id]
        if task.status != Status.RUNNING: raise RuntimeError("task is not running")
        task.lease_until = (time() if now is None else now) + self.lease_seconds

    def finish(self, task_id: str, result: str) -> None:
        task = self.tasks[task_id]
        if task.status != Status.RUNNING: raise RuntimeError("task is not running")
        task.status, task.result = Status.SUCCEEDED, result

    def fail(self, task_id: str, error: str) -> None:
        task = self.tasks[task_id]
        if task.status != Status.RUNNING: raise RuntimeError("task is not running")
        task.status, task.error = Status.FAILED, error

    def cancel(self, task_id: str) -> None:
        task = self.tasks[task_id]
        if task.status in (Status.SUCCEEDED, Status.CANCELLED): raise RuntimeError("terminal task")
        task.status = Status.CANCELLED

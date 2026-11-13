"""Capability-aware task delegation with leases and bounded retries."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

class Status(str, Enum):
    QUEUED = "queued"
    LEASED = "leased"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

@dataclass(frozen=True)
class Worker:
    worker_id: str
    capabilities: frozenset[str]
    capacity: int = 1

@dataclass
class Task:
    task_id: str
    required: frozenset[str]
    payload: dict
    max_attempts: int = 2
    attempts: int = 0
    status: Status = Status.QUEUED
    worker_id: str | None = None
    result: object = None
    error: str | None = None

@dataclass
class DelegationCoordinator:
    workers: dict[str, Worker]
    tasks: dict[str, Task] = field(default_factory=dict)

    def __post_init__(self):
        if any(w.capacity < 1 for w in self.workers.values()):
            raise ValueError("worker capacity must be positive")

    def submit(self, task: Task) -> None:
        if not task.task_id or task.task_id in self.tasks:
            raise ValueError("task_id must be non-empty and unique")
        if task.max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        self.tasks[task.task_id] = task

    def delegate(self, task_id: str) -> str:
        task = self.tasks[task_id]
        if task.status != Status.QUEUED:
            raise ValueError("only queued tasks can be delegated")
        active = {t.worker_id for t in self.tasks.values() if t.status == Status.LEASED}
        candidates = [w for w in self.workers.values()
                      if task.required <= w.capabilities
                      and sum(1 for t in self.tasks.values()
                              if t.status == Status.LEASED and t.worker_id == w.worker_id) < w.capacity]
        if not candidates:
            raise RuntimeError("no capable worker has available capacity")
        worker = sorted(candidates, key=lambda w: (w.worker_id in active, w.worker_id))[0]
        task.worker_id = worker.worker_id
        task.attempts += 1
        task.status = Status.LEASED
        task.error = None
        return worker.worker_id

    def complete(self, task_id: str, worker_id: str, result: object) -> None:
        task = self.tasks[task_id]
        self._assert_lease(task, worker_id)
        task.result, task.status = result, Status.SUCCEEDED

    def reject(self, task_id: str, worker_id: str, reason: str) -> None:
        task = self.tasks[task_id]
        self._assert_lease(task, worker_id)
        task.error, task.worker_id = reason, None
        task.status = Status.QUEUED if task.attempts < task.max_attempts else Status.FAILED

    def _assert_lease(self, task: Task, worker_id: str) -> None:
        if task.status != Status.LEASED or task.worker_id != worker_id:
            raise ValueError("worker does not hold this task lease")

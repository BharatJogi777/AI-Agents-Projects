"""Checkpointable research task state; evidence is supplied, never fabricated."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ResearchTask:
    task_id: str
    description: str
    status: str = "pending"
    evidence_refs: tuple[str, ...] = ()

@dataclass(frozen=True)
class ResearchRun:
    run_id: str
    tasks: tuple[ResearchTask, ...]

def checkpoint_run(run_id: str, tasks: list[ResearchTask]) -> ResearchRun:
    if not run_id.strip() or not tasks:
        raise ValueError("run_id and at least one task are required")
    seen=set()
    allowed={"pending","running","blocked","completed","failed"}
    for task in tasks:
        if not task.task_id.strip() or task.task_id in seen:
            raise ValueError("task IDs must be non-empty and unique")
        seen.add(task.task_id)
        if not task.description.strip() or task.status not in allowed:
            raise ValueError("task description or status is invalid")
        if any(not ref.strip() for ref in task.evidence_refs):
            raise ValueError("evidence references cannot be empty")
        if task.status == "completed" and not task.evidence_refs:
            raise ValueError("completed research tasks require evidence references")
    return ResearchRun(run_id, tuple(tasks))

def resumable_tasks(run: ResearchRun) -> tuple[str, ...]:
    return tuple(t.task_id for t in run.tasks if t.status in {"pending","blocked","failed"})

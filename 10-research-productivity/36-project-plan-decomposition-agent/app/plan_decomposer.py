"""Decompose a project goal into a validated, dependency-aware plan."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    id: str
    title: str
    depends_on: tuple[str, ...] = ()
    owner: str | None = None
    estimate_hours: float | None = None
    acceptance_criteria: tuple[str, ...] = ()

def decompose_plan(tasks: list[Task]) -> list[Task]:
    """Validate references and return a stable topological task order."""
    if not tasks:
        raise ValueError("at least one task is required")
    by_id = {}
    for task in tasks:
        if not task.id.strip() or not task.title.strip():
            raise ValueError("task id and title must be non-empty")
        if task.id in by_id:
            raise ValueError(f"duplicate task id: {task.id}")
        if task.estimate_hours is not None and task.estimate_hours < 0:
            raise ValueError("estimate_hours cannot be negative")
        by_id[task.id] = task
    for task in tasks:
        unknown = set(task.depends_on) - by_id.keys()
        if unknown:
            raise ValueError(f"unknown dependencies for {task.id}: {sorted(unknown)}")
        if task.id in task.depends_on:
            raise ValueError(f"task cannot depend on itself: {task.id}")
    ordered, remaining = [], {t.id: set(t.depends_on) for t in tasks}
    while remaining:
        ready = [t.id for t in tasks if t.id in remaining and not remaining[t.id]]
        if not ready:
            raise ValueError("dependency cycle detected")
        for task_id in ready:
            ordered.append(by_id[task_id])
            remaining.pop(task_id)
            for deps in remaining.values():
                deps.discard(task_id)
    return ordered

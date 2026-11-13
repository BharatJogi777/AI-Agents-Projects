"""Explainable task ranking based only on supplied prioritization signals."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    task_id: str
    title: str
    urgency: int
    impact: int
    effort_hours: float
    due_in_days: int

@dataclass(frozen=True)
class RankedTask:
    task: Task
    score: float
    reasons: tuple[str, ...]

def prioritize(tasks: list[Task]) -> tuple[RankedTask, ...]:
    seen=set(); ranked=[]
    for task in tasks:
        if not task.task_id.strip() or task.task_id in seen:
            raise ValueError("task IDs must be non-empty and unique")
        seen.add(task.task_id)
        if not task.title.strip() or not 1 <= task.urgency <= 5 or not 1 <= task.impact <= 5:
            raise ValueError("title and urgency/impact scores are invalid")
        if task.effort_hours <= 0 or task.due_in_days < 0:
            raise ValueError("effort must be positive and due_in_days non-negative")
        score = task.urgency * 3 + task.impact * 2 + min(10, 10 / task.effort_hours) + (5 if task.due_in_days <= 1 else 0)
        reasons=(f"urgency={task.urgency}/5",f"impact={task.impact}/5",f"effort_hours={task.effort_hours:g}",f"due_in_days={task.due_in_days}")
        ranked.append(RankedTask(task,round(score,2),reasons))
    ranked.sort(key=lambda r:(-r.score,r.task.task_id))
    return tuple(ranked)

"""Validate cross-session continuation snapshots without executing tasks."""
from dataclasses import dataclass

@dataclass(frozen=True)
class TaskSnapshot:
    task_id: str
    version: int
    status: str
    checkpoint: str
    required_context: tuple[str, ...]

def validate_resume(snapshot: TaskSnapshot, *, available_context: set[str], supported_version: int = 1) -> tuple[bool, tuple[str, ...]]:
    if not snapshot.task_id.strip() or snapshot.version < 1:
        raise ValueError("task_id and positive version are required")
    if snapshot.status not in {"pending","running","paused","completed","failed"}:
        raise ValueError("unsupported task status")
    if snapshot.version != supported_version:
        return False, ("snapshot_version_mismatch",)
    if snapshot.status == "completed":
        return False, ("task_already_completed",)
    missing = tuple(sorted(set(snapshot.required_context) - available_context))
    if missing:
        return False, tuple(f"missing_context:{item}" for item in missing)
    if snapshot.status == "failed":
        return False, ("failed_task_requires_review",)
    if snapshot.status == "running" and not snapshot.checkpoint.strip():
        return False, ("running_task_missing_checkpoint",)
    return True, ()

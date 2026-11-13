"""Inspect workflow snapshots; this module never changes execution state."""
from dataclasses import dataclass

@dataclass(frozen=True)
class StepSnapshot:
    step_id: str
    status: str
    elapsed_seconds: int
    timeout_seconds: int

@dataclass(frozen=True)
class Finding:
    step_id: str
    severity: str
    message: str

def inspect_workflow(steps: list[StepSnapshot]) -> tuple[Finding, ...]:
    if not steps:
        raise ValueError("at least one workflow step is required")
    seen, findings=set(), []
    allowed={"pending","running","completed","failed","cancelled"}
    for step in steps:
        if not step.step_id.strip() or step.step_id in seen:
            raise ValueError("step IDs must be non-empty and unique")
        seen.add(step.step_id)
        if step.status not in allowed or step.elapsed_seconds < 0 or step.timeout_seconds <= 0:
            raise ValueError("invalid status or timing")
        if step.status == "running" and step.elapsed_seconds > step.timeout_seconds:
            findings.append(Finding(step.step_id,"high","Running step exceeded its timeout"))
        elif step.status == "failed":
            findings.append(Finding(step.step_id,"high","Step reported failure"))
        elif step.status == "pending" and step.elapsed_seconds > step.timeout_seconds:
            findings.append(Finding(step.step_id,"medium","Pending step may be stalled"))
    return tuple(findings)

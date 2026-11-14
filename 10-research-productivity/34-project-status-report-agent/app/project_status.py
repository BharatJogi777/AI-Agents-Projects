"""Build a project status report from supplied workstream facts."""
from dataclasses import dataclass

@dataclass(frozen=True)
class StatusReport:
    project: str
    overall_status: str
    completed: tuple[str,...]
    in_progress: tuple[str,...]
    blocked: tuple[str,...]
    next_steps: tuple[str,...]

def build_status_report(*, project: str, overall_status: str, completed: list[str], in_progress: list[str], blocked: list[str], next_steps: list[str]) -> StatusReport:
    if not isinstance(project,str) or not project.strip(): raise ValueError("project is required")
    if overall_status not in ("on_track","at_risk","blocked","completed"): raise ValueError("invalid overall status")
    groups={"completed":completed,"in_progress":in_progress,"blocked":blocked,"next_steps":next_steps}
    for name,items in groups.items():
        if not isinstance(items,list) or any(not isinstance(x,str) or not x.strip() for x in items): raise ValueError(f"{name} must contain non-empty strings")
    return StatusReport(project.strip(),overall_status,*(tuple(x.strip() for x in groups[k]) for k in ("completed","in_progress","blocked","next_steps")))

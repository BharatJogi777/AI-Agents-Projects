"""Build a dry-run desktop workflow from explicitly allowlisted steps."""
from dataclasses import dataclass
from typing import Iterable

ALLOWED={"launch_application","open_document","copy_text","wait"}
@dataclass(frozen=True)
class Step:
    action: str
    target: str
    value: str = ""

def validate_workflow(steps: Iterable[Step], *, allowed_targets: set[str], max_steps: int = 20) -> tuple[Step,...]:
    items=tuple(steps)
    if not items or len(items)>max_steps or max_steps<1:
        raise ValueError("workflow must contain 1..max_steps steps")
    for step in items:
        if step.action not in ALLOWED:
            raise ValueError(f"unsupported action: {step.action}")
        if not step.target or step.target not in allowed_targets:
            raise ValueError(f"target is not allowlisted: {step.target}")
        if step.action=="wait":
            try:
                seconds=float(step.value)
            except ValueError as exc:
                raise ValueError("wait value must be numeric seconds") from exc
            if not 0 <= seconds <= 30:
                raise ValueError("wait must be between 0 and 30 seconds")
    return items

def dry_run(steps: Iterable[Step], *, allowed_targets: set[str]) -> list[dict[str,str]]:
    return [{"step":str(i),"action":s.action,"target":s.target,"value":s.value,"status":"awaiting_user_approval"} for i,s in enumerate(validate_workflow(steps,allowed_targets=allowed_targets),1)]

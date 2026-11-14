"""Produce a safe cleanup plan for supplied knowledge-base records."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CleanupAction:
    record_id: str
    action: str
    reason: str

def plan_cleanup(*, records: list[dict[str, str]], required_fields: tuple[str, ...] = ("id", "title", "body")) -> tuple[CleanupAction, ...]:
    if not isinstance(records, list) or not isinstance(required_fields, tuple) or not required_fields:
        raise ValueError("records must be a list and required_fields a non-empty tuple")
    if any(not isinstance(f, str) or not f.strip() for f in required_fields):
        raise ValueError("required field names must be non-empty strings")
    seen=set(); actions=[]
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError("each record must be a mapping")
        rid=record.get("id", f"row-{index+1}")
        if not isinstance(rid, str) or not rid.strip():
            raise ValueError("record IDs must be non-empty strings")
        missing=[f for f in required_fields if not isinstance(record.get(f), str) or not record[f].strip()]
        if rid in seen:
            actions.append(CleanupAction(rid, "manual_review", "duplicate record ID"))
        elif missing:
            actions.append(CleanupAction(rid, "manual_review", "missing or blank fields: "+", ".join(missing)))
        else:
            actions.append(CleanupAction(rid, "keep", "required fields present"))
        seen.add(rid)
    return tuple(actions)

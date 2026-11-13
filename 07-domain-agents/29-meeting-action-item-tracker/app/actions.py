from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class ActionItem:
    action_id: str
    description: str
    owner: str
    due_date: date
    status: str = "open"
def track(items: list[ActionItem], as_of: date | None = None) -> dict:
    as_of=as_of or date.today(); seen=set(); rows=[]
    allowed={"open","in_progress","blocked","done"}
    for x in items:
        if not all(v.strip() for v in (x.action_id,x.description,x.owner)): raise ValueError("action_id, description and owner are required")
        if x.action_id in seen: raise ValueError(f"duplicate action_id: {x.action_id}")
        if x.status not in allowed: raise ValueError("unsupported status")
        seen.add(x.action_id)
        state="overdue" if x.status!="done" and x.due_date<as_of else x.status
        rows.append({"action_id":x.action_id,"description":x.description,"owner":x.owner,"due_date":x.due_date.isoformat(),"status":state})
    rows.sort(key=lambda x:(x["due_date"],x["action_id"]))
    return {"items":rows,"open_count":sum(x["status"]!="done" for x in rows),"overdue_count":sum(x["status"]=="overdue" for x in rows)}

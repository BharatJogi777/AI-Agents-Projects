from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class OnboardingTask:
    task_id: str
    title: str
    owner: str
    due_date: date
    required: bool = True
    completed: bool = False
def build_checklist(tasks: list[OnboardingTask], start_date: date, as_of: date | None = None) -> dict:
    as_of=as_of or date.today(); seen=set(); rows=[]
    for t in tasks:
        if not t.task_id.strip() or not t.title.strip() or not t.owner.strip(): raise ValueError("task_id, title and owner are required")
        if t.task_id in seen: raise ValueError(f"duplicate task_id: {t.task_id}")
        if t.due_date<start_date: raise ValueError("task due date cannot precede onboarding start")
        seen.add(t.task_id)
        state="complete" if t.completed else ("overdue" if t.due_date<as_of else "pending")
        rows.append({"task_id":t.task_id,"title":t.title,"owner":t.owner,"due_date":t.due_date.isoformat(),"required":t.required,"status":state})
    rows.sort(key=lambda x:(x["due_date"],x["task_id"]))
    return {"tasks":rows,"required_open":sum(x["required"] and x["status"]!="complete" for x in rows),"human_confirmation_required":True}

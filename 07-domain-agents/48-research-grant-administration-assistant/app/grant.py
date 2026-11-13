from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class GrantMilestone:
    milestone_id: str
    grant_id: str
    description: str
    due_date: date
    owner: str
    evidence_ref: str | None
def review_milestones(items: list[GrantMilestone], as_of: date) -> dict:
    seen=set(); rows=[]
    for m in items:
        if not all(x.strip() for x in (m.milestone_id,m.grant_id,m.description,m.owner)): raise ValueError("milestone, grant, description and owner are required")
        if m.milestone_id in seen: raise ValueError("duplicate milestone id")
        seen.add(m.milestone_id); overdue=m.due_date<as_of
        rows.append({"milestone_id":m.milestone_id,"grant_id":m.grant_id,"owner":m.owner,"due_date":m.due_date.isoformat(),"overdue":overdue,"evidence_missing":not bool(m.evidence_ref and m.evidence_ref.strip()),"status":"attention_required" if overdue or not (m.evidence_ref and m.evidence_ref.strip()) else "recorded"})
    return {"milestones":rows,"attention_count":sum(x["status"]=="attention_required" for x in rows),"report_submitted":False,"financial_approval_granted":False}

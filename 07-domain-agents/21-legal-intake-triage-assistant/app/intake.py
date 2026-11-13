from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class Intake:
    matter_type: str
    summary: str
    received_on: date
    deadline: date | None = None
    jurisdiction: str | None = None
    opposing_party: str | None = None
def triage(item: Intake, today: date | None = None) -> dict:
    today = today or date.today()
    if not item.matter_type.strip() or not item.summary.strip(): raise ValueError("matter_type and summary are required")
    if item.deadline and item.deadline < item.received_on: raise ValueError("deadline cannot precede received date")
    days = (item.deadline-today).days if item.deadline else None
    missing = [k for k,v in (("jurisdiction",item.jurisdiction),("opposing_party",item.opposing_party)) if not v or not v.strip()]
    urgency = "past_deadline_review" if days is not None and days < 0 else ("urgent" if days is not None and days <= 7 else "standard")
    return {"matter_type":item.matter_type.strip(),"urgency":urgency,"days_to_deadline":days,"missing_fields":missing,"requires_conflict_check":True,"human_review_required":True,"legal_advice_provided":False}

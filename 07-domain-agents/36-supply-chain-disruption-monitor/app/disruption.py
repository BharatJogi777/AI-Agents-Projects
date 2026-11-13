from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class SupplyEvent:
    event_id: str
    supplier: str
    component: str
    reported_on: date
    impact_days: int
    severity: int
    source_ref: str
def assess_events(events: list[SupplyEvent], as_of: date | None = None) -> dict:
    as_of=as_of or date.today(); seen=set(); rows=[]
    for e in events:
        if not all(x.strip() for x in (e.event_id,e.supplier,e.component,e.source_ref)): raise ValueError("event, supplier, component and source reference are required")
        if e.event_id in seen: raise ValueError(f"duplicate event_id: {e.event_id}")
        if e.impact_days<0 or not 1<=e.severity<=5: raise ValueError("impact_days must be non-negative and severity between 1 and 5")
        if e.reported_on>as_of: raise ValueError("reported_on cannot be in the future")
        seen.add(e.event_id)
        score=e.impact_days*e.severity
        rows.append({"event_id":e.event_id,"supplier":e.supplier,"component":e.component,"risk_score":score,"risk":"critical" if score>=20 else ("elevated" if score>=8 else "monitor"),"source_ref":e.source_ref})
    rows.sort(key=lambda x:(-x["risk_score"],x["event_id"]))
    return {"events":rows,"human_review_required":True,"supplier_action_taken":False}

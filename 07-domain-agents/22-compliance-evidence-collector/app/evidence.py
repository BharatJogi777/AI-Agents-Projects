from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class Evidence:
    control_id: str
    source: str
    collected_on: date
    expires_on: date | None = None
    reviewer: str | None = None
def assess_evidence(items: list[Evidence], as_of: date | None = None) -> dict:
    as_of=as_of or date.today(); seen=set(); rows=[]
    for e in items:
        if not e.control_id.strip() or not e.source.strip(): raise ValueError("control_id and source are required")
        if e.expires_on and e.expires_on<e.collected_on: raise ValueError("expiry cannot precede collection")
        if e.control_id in seen: raise ValueError(f"duplicate control_id: {e.control_id}")
        seen.add(e.control_id)
        state="expired" if e.expires_on and e.expires_on<as_of else ("pending_review" if not e.reviewer else "reviewed")
        rows.append({"control_id":e.control_id,"source":e.source,"status":state,"reviewer":e.reviewer})
    return {"items":rows,"total":len(rows),"pending_review":sum(x["status"]=="pending_review" for x in rows),"expired":sum(x["status"]=="expired" for x in rows),"certification":False}

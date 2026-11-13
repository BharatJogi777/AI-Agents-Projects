from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True)
class Observation:
    observation_id: str
    field_id: str
    observed_at: datetime
    category: str
    severity: int
    note: str
    evidence_ref: str
def review_observations(items: list[Observation], as_of: datetime) -> dict:
    seen=set(); rows=[]
    allowed={"pest","disease","water","nutrient","weather","equipment","other"}
    for x in items:
        if not all(v.strip() for v in (x.observation_id,x.field_id,x.note,x.evidence_ref)): raise ValueError("observation, field, note and evidence reference are required")
        if x.observation_id in seen: raise ValueError("duplicate observation id")
        if x.category not in allowed or not 1<=x.severity<=5: raise ValueError("invalid category or severity")
        if x.observed_at>as_of: raise ValueError("observation cannot be in the future")
        seen.add(x.observation_id)
        rows.append({"observation_id":x.observation_id,"field_id":x.field_id,"category":x.category,"severity":x.severity,"priority":"urgent_review" if x.severity>=4 else ("review" if x.severity>=2 else "log"),"evidence_ref":x.evidence_ref,"recommendation":"Request agronomist review" if x.category in {"pest","disease"} and x.severity>=3 else "Record and monitor"})
    rows.sort(key=lambda r:(-r["severity"],r["observation_id"]))
    return {"observations":rows,"human_review_required":True,"treatment_recommended":False}

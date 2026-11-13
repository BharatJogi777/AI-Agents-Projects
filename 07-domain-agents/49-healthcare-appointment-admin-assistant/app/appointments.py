from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True)
class Appointment:
    appointment_id: str
    patient_reference: str
    starts_at: datetime
    ends_at: datetime
    status: str
    provider_reference: str
def validate_schedule(items: list[Appointment]) -> dict:
    seen=set(); by_provider={}; rows=[]
    allowed={"requested","confirmed","cancelled","completed"}
    for a in items:
        if not all(x.strip() for x in (a.appointment_id,a.patient_reference,a.provider_reference)): raise ValueError("appointment, patient and provider references are required")
        if a.appointment_id in seen: raise ValueError("duplicate appointment id")
        if a.ends_at<=a.starts_at: raise ValueError("appointment end must follow start")
        if a.status not in allowed: raise ValueError("invalid appointment status")
        seen.add(a.appointment_id)
        conflict=False
        if a.status not in {"cancelled","completed"}:
            for old in by_provider.setdefault(a.provider_reference,[]):
                if a.starts_at<old.ends_at and old.starts_at<a.ends_at: conflict=True
            by_provider[a.provider_reference].append(a)
        rows.append({"appointment_id":a.appointment_id,"provider_reference":a.provider_reference,"status":a.status,"overlap_conflict":conflict,"manual_follow_up":conflict or a.status=="requested"})
    return {"appointments":rows,"conflict_count":sum(x["overlap_conflict"] for x in rows),"booking_created":False,"patient_notified":False}

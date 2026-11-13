"""Explainable incident severity classification from structured evidence."""
from dataclasses import dataclass

@dataclass(frozen=True)
class IncidentSignals:
    affected_users: int
    total_users: int
    critical_service: bool
    data_loss_suspected: bool
    duration_minutes: int
    workaround_available: bool

def classify_severity(s: IncidentSignals) -> dict:
    for name,value in (("affected_users",s.affected_users),("total_users",s.total_users),("duration_minutes",s.duration_minutes)):
        if not isinstance(value,int) or value < 0: raise ValueError(f"{name} must be a non-negative integer")
    if s.total_users == 0 or s.affected_users > s.total_users: raise ValueError("affected_users must not exceed positive total_users")
    if s.duration_minutes < 0: raise ValueError("duration_minutes must be non-negative")
    ratio=s.affected_users/s.total_users
    score=0; reasons=[]
    if s.critical_service: score+=3; reasons.append("critical service affected")
    if s.data_loss_suspected: score+=4; reasons.append("possible data loss")
    if ratio >= .5: score+=3; reasons.append("at least half of users affected")
    elif ratio >= .1: score+=2; reasons.append("at least ten percent of users affected")
    elif s.affected_users: score+=1; reasons.append("some users affected")
    if s.duration_minutes >= 60: score+=2; reasons.append("duration at least one hour")
    elif s.duration_minutes >= 15: score+=1; reasons.append("duration at least fifteen minutes")
    if s.workaround_available: score-=1; reasons.append("workaround available")
    severity="SEV1" if score>=7 else "SEV2" if score>=4 else "SEV3" if score>=2 else "SEV4"
    return {"severity":severity,"score":max(0,score),"reasons":reasons,"affected_ratio":ratio,"requires_human_confirmation":True}

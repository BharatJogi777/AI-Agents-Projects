"""Check data records against declared retention rules."""
from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class RetentionRecord:
 record_id:str; created_on:date; legal_hold:bool=False
@dataclass(frozen=True)
class RetentionDecision:
 record_id:str; action:str; expires_on:date; reason:str
def evaluate_retention(records:list[RetentionRecord],*,retention_days:int,as_of:date)->tuple[RetentionDecision,...]:
 if isinstance(retention_days,bool) or not isinstance(retention_days,int) or retention_days<0: raise ValueError("retention_days must be a non-negative integer")
 ids=[r.record_id for r in records]
 if any(not x for x in ids) or len(ids)!=len(set(ids)): raise ValueError("record IDs must be unique and non-empty")
 result=[]
 from datetime import timedelta
 for r in records:
  if r.created_on>as_of: raise ValueError("record creation date cannot be in the future")
  expiry=r.created_on+timedelta(days=retention_days)
  if r.legal_hold: action,reason="retain","legal_hold"
  elif as_of>expiry: action,reason="eligible_for_deletion_review","retention_expired"
  else: action,reason="retain","within_retention_period"
  result.append(RetentionDecision(r.record_id,action,expiry,reason))
 return tuple(result)

"""Explainable account health summary from explicitly supplied signals."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AccountHealth:
    score: int
    status: str
    positive_signals: tuple[str,...]
    risk_signals: tuple[str,...]
    missing_signals: tuple[str,...]

def summarize_account_health(*, usage_trend: str|None, support_trend: str|None, stakeholder_engagement: str|None, renewal_days: int|None, payment_status: str|None) -> AccountHealth:
    allowed={"usage_trend":{"growing","stable","declining"},"support_trend":{"improving","stable","worsening"},"stakeholder_engagement":{"strong","moderate","weak"},"payment_status":{"current","late","overdue"}}
    vals=locals()
    for field,choices in allowed.items():
        value=vals[field]
        if value is not None and value not in choices: raise ValueError(f"invalid {field}")
    if renewal_days is not None and (isinstance(renewal_days,bool) or not isinstance(renewal_days,int) or renewal_days<0): raise ValueError("renewal_days must be a non-negative integer")
    missing=tuple(k for k in (*allowed.keys(),"renewal_days") if vals[k] is None)
    positive=[]; risks=[]; score=50
    for field,value,good,bad,points in [("usage",usage_trend,"growing","declining",15),("support",support_trend,"improving","worsening",10),("engagement",stakeholder_engagement,"strong","weak",15),("payment",payment_status,"current","overdue",15)]:
        if value is None: continue
        if value==good: score+=points; positive.append(f"{field.title()} signal is {value}.")
        elif value==bad: score-=points; risks.append(f"{field.title()} signal is {value}.")
        else: positive.append(f"{field.title()} signal is stable or moderate.")
    if renewal_days is not None:
        if renewal_days<=30: risks.append("Renewal is within 30 days."); score-=10
        elif renewal_days<=90: risks.append("Renewal is within 90 days."); score-=5
    score=max(0,min(100,score)); status="healthy" if score>=70 else "at_risk" if score>=40 else "critical"
    if missing: risks.append("Health view is incomplete; missing signals: "+", ".join(missing)+".")
    return AccountHealth(score,status,tuple(positive),tuple(risks),missing)

"""Evaluate certificate inventory dates; date values must be ISO-8601 dates."""
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class CertificateFinding:
    certificate_id: str
    days_remaining: int
    severity: str
    message: str

def check_expiry(certificates: list[dict], *, today: date, warning_days: int=30) -> list[CertificateFinding]:
    if not isinstance(today,date): raise TypeError("today must be a date")
    if warning_days<0: raise ValueError("warning_days must be non-negative")
    if not isinstance(certificates,list): raise TypeError("certificates must be a list")
    out=[]; seen=set()
    for i,c in enumerate(certificates):
        if not isinstance(c,dict): raise ValueError(f"certificate {i} must be an object")
        cid=c.get("id"); raw=c.get("expires_on")
        if not isinstance(cid,str) or not cid.strip() or cid in seen: raise ValueError(f"certificate {i} requires unique id")
        seen.add(cid)
        try: expiry=date.fromisoformat(raw)
        except (TypeError,ValueError): raise ValueError(f"certificate {cid}: expires_on must be YYYY-MM-DD")
        days=(expiry-today).days
        if days<0: out.append(CertificateFinding(cid,days,"critical","Certificate has expired; rotate and verify dependent services."))
        elif days<=warning_days: out.append(CertificateFinding(cid,days,"high" if days<=7 else "medium","Certificate is approaching expiry; schedule renewal and validate deployment."))
    return sorted(out,key=lambda x:x.days_remaining)

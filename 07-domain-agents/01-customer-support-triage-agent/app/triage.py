"""Rule-based ticket triage with explainable routing."""
from dataclasses import dataclass

@dataclass(frozen=True)
class TriageResult:
    category: str
    priority: str
    team: str
    reasons: tuple[str,...]

def triage_ticket(subject: str, message: str, *, customer_tier: str="standard", has_outage_signal: bool=False) -> TriageResult:
    if not isinstance(subject,str) or not subject.strip() or not isinstance(message,str) or not message.strip(): raise ValueError("subject and message are required")
    if customer_tier not in {"standard","premium","enterprise"} or not isinstance(has_outage_signal,bool): raise ValueError("invalid customer tier or outage flag")
    text=(subject+" "+message).lower(); rules={
      "billing":(["invoice","charged","payment","billing"],"Billing"),
      "technical":(["error","bug","crash","not working","timeout","login"],"Technical Support"),
      "delivery":(["delivery","shipment","tracking","late order"],"Fulfillment"),
      "account":(["password","account","profile","access"],"Account Support")}
    category,team="general","Customer Support"; reasons=[]
    for name,(terms,owner) in rules.items():
        if any(term in text for term in terms): category,team=name,owner; reasons.append(f"Matched {name} support keywords."); break
    urgent=has_outage_signal or any(x in text for x in ("cannot access","service down","data loss","security breach"))
    if urgent: priority="urgent"; reasons.append("Urgent operational or customer-impact phrase detected.")
    elif any(x in text for x in ("as soon as possible","urgent","today")): priority="high"; reasons.append("Customer requested prompt attention.")
    elif customer_tier=="enterprise": priority="high"; reasons.append("Enterprise tier escalation policy applied.")
    else: priority="normal"
    if customer_tier!="standard": reasons.append(f"{customer_tier.title()} customer tier noted for routing review.")
    return TriageResult(category,priority,team,tuple(reasons))

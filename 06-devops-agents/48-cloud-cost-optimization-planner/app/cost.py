"""Generate cost optimization opportunities from supplied inventory metrics."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CostOpportunity:
    resource_id: str
    action: str
    estimated_monthly_savings: float
    rationale: str
    requires_owner_review: bool=True

def plan_cost_optimizations(resources: list[dict], *, low_utilization_percent: float=15.0, idle_days: int=14) -> list[CostOpportunity]:
    if not isinstance(resources,list): raise TypeError("resources must be a list")
    if not 0<=low_utilization_percent<=100 or isinstance(idle_days,bool) or not isinstance(idle_days,int) or idle_days<1: raise ValueError("invalid thresholds")
    out=[]; seen=set()
    for i,r in enumerate(resources):
        if not isinstance(r,dict): raise ValueError(f"resource {i} must be an object")
        rid=r.get("resource_id"); cost=r.get("monthly_cost"); util=r.get("average_utilization_percent"); idle=r.get("idle_days"); kind=r.get("kind","compute")
        if not isinstance(rid,str) or not rid or rid in seen: raise ValueError("resource_id must be unique and non-empty")
        seen.add(rid)
        if isinstance(cost,bool) or not isinstance(cost,(int,float)) or cost<0: raise ValueError(f"{rid}: invalid monthly_cost")
        if isinstance(util,bool) or not isinstance(util,(int,float)) or not 0<=util<=100: raise ValueError(f"{rid}: invalid utilization")
        if isinstance(idle,bool) or not isinstance(idle,int) or idle<0: raise ValueError(f"{rid}: invalid idle_days")
        if idle>=idle_days: action="review_for_decommission"; saving=float(cost); why=f"Resource has been idle for {idle} days."
        elif util<=low_utilization_percent and kind=="compute": action="review_rightsizing"; saving=float(cost)*0.25; why=f"Average utilization is {util}%."
        else: continue
        out.append(CostOpportunity(rid,action,round(saving,2),why))
    return out

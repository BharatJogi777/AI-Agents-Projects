"""Validate and rank a project risk register using likelihood and impact."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Risk:
    risk_id: str
    description: str
    likelihood: int
    impact: int
    score: int
    priority: str

def build_risk_register(*, risks: list[dict]) -> tuple[Risk,...]:
    if not isinstance(risks,list): raise ValueError("risks must be a list")
    result=[]; seen=set()
    for r in risks:
        if not isinstance(r,dict): raise ValueError("each risk must be a mapping")
        rid,desc,likelihood,impact=(r.get(k) for k in ("id","description","likelihood","impact"))
        if not isinstance(rid,str) or not rid.strip() or not isinstance(desc,str) or not desc.strip(): raise ValueError("risk ID and description are required")
        if rid in seen: raise ValueError("risk IDs must be unique")
        if any(not isinstance(x,int) or isinstance(x,bool) or not 1<=x<=5 for x in (likelihood,impact)): raise ValueError("likelihood and impact must be integers from 1 to 5")
        seen.add(rid); score=likelihood*impact
        priority="critical" if score>=20 else "high" if score>=12 else "medium" if score>=6 else "low"
        result.append(Risk(rid,desc.strip(),likelihood,impact,score,priority))
    return tuple(sorted(result,key=lambda x:(-x.score,x.risk_id)))

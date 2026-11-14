"""Build a validated and consistently prioritized model risk register."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Risk:
 risk_id:str; title:str; likelihood:int; impact:int; owner:str; mitigation:str
@dataclass(frozen=True)
class RiskEntry:
 risk_id:str; title:str; score:int; level:str; owner:str; mitigation:str
def generate_register(risks:list[Risk])->tuple[RiskEntry,...]:
 ids=[r.risk_id for r in risks]
 if any(not x for x in ids) or len(ids)!=len(set(ids)): raise ValueError("risk IDs must be unique and non-empty")
 result=[]
 for r in risks:
  if not r.title.strip() or not r.owner.strip() or not r.mitigation.strip(): raise ValueError("title, owner, and mitigation are required")
  if any(isinstance(x,bool) or not isinstance(x,int) or not 1<=x<=5 for x in (r.likelihood,r.impact)): raise ValueError("likelihood and impact must be integers from 1 to 5")
  score=r.likelihood*r.impact; level="critical" if score>=20 else "high" if score>=12 else "medium" if score>=6 else "low"
  result.append(RiskEntry(r.risk_id,r.title,score,level,r.owner,r.mitigation))
 return tuple(sorted(result,key=lambda x:(-x.score,x.risk_id)))

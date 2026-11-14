"""Filter a caller-supplied grant catalogue against explicit criteria."""
from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class Grant:
    id:str; title:str; topics:tuple[str,...]; eligible_applicants:tuple[str,...]; min_funding:float; max_funding:float; deadline:date|None
def find_grants(grants:list[Grant],*,applicant_type:str,topic:str,budget:float,as_of:date)->list[Grant]:
    if not applicant_type.strip() or not topic.strip() or budget<0: raise ValueError("applicant_type/topic are required and budget cannot be negative")
    seen=set(); matches=[]
    for g in grants:
        if not g.id.strip() or not g.title.strip() or g.id in seen: raise ValueError("grant ids and titles must be non-empty and ids unique")
        seen.add(g.id)
        if g.min_funding<0 or g.max_funding<g.min_funding: raise ValueError(f"invalid funding range for {g.id}")
        if g.deadline is not None and g.deadline<as_of: continue
        if applicant_type.casefold() not in {v.casefold() for v in g.eligible_applicants}: continue
        if topic.casefold() not in {v.casefold() for v in g.topics}: continue
        if g.min_funding<=budget<=g.max_funding: matches.append(g)
    return sorted(matches,key=lambda g:(g.deadline or date.max,g.id))

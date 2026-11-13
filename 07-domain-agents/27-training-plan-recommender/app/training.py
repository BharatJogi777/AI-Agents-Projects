from dataclasses import dataclass
@dataclass(frozen=True)
class SkillGap:
    skill: str
    current_level: int
    target_level: int
    priority: int = 3
def recommend(gaps: list[SkillGap], catalog: list[dict]) -> dict:
    plans=[]; seen=set()
    for g in gaps:
        key=g.skill.strip().casefold()
        if not key or not 0<=g.current_level<=5 or not 1<=g.target_level<=5 or not 1<=g.priority<=5: raise ValueError("invalid skill gap")
        if key in seen: raise ValueError(f"duplicate skill: {g.skill}")
        seen.add(key)
        if g.target_level<=g.current_level: continue
        options=[c for c in catalog if key in [s.casefold() for s in c.get("skills",[])]]
        options.sort(key=lambda c:(c.get("duration_hours",10**9),c.get("id","")))
        plans.append({"skill":g.skill,"gap":g.target_level-g.current_level,"priority":g.priority,"resources":[{"id":c["id"],"title":c.get("title",""),"duration_hours":c.get("duration_hours")} for c in options if c.get("id")]})
    plans.sort(key=lambda x:(-x["priority"],-x["gap"],x["skill"].casefold()))
    return {"recommendations":plans,"manager_review_required":True,"automatic_enrollment":False}

from dataclasses import dataclass
@dataclass(frozen=True)
class LearningObjective:
    objective_id: str
    description: str
    prerequisites: tuple[str,...]
    mastery_threshold: float
def build_learning_path(objectives: list[LearningObjective], mastered: set[str]) -> dict:
    by_id={}
    for o in objectives:
        if not o.objective_id.strip() or o.objective_id in by_id: raise ValueError("objective ids must be non-empty and unique")
        if not o.description.strip() or not 0<=o.mastery_threshold<=1: raise ValueError("description and valid mastery threshold required")
        by_id[o.objective_id]=o
    unknown={p for o in objectives for p in o.prerequisites if p not in by_id}
    if unknown: raise ValueError(f"unknown prerequisites: {sorted(unknown)}")
    if mastered-set(by_id): raise ValueError("mastered contains unknown objective ids")
    remaining=set(by_id); completed=set(mastered); ordered=[]
    while remaining:
        ready=sorted(k for k in remaining if set(by_id[k].prerequisites)<=completed)
        if not ready: raise ValueError("prerequisite cycle detected")
        for k in ready:
            ordered.append({"objective_id":k,"description":by_id[k].description,"mastery_threshold":by_id[k].mastery_threshold,"status":"mastered" if k in mastered else "ready"})
        completed.update(ready); remaining.difference_update(ready)
    return {"learning_path":ordered,"assessment_required_before_mastery":True,"grades_assigned":False}

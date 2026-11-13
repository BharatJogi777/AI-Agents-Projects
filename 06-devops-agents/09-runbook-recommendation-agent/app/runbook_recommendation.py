"""Evidence-linked runbook recommendation; suggestions only, never execution."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Procedure:
    procedure_id: str
    title: str
    symptom_tags: tuple[str,...]
    prerequisites: tuple[str,...] = ()
    risk: str = "medium"

def recommend_runbooks(symptoms: list[str], procedures: list[Procedure], *, max_results: int = 5) -> list[dict]:
    if not 1 <= max_results <= 20: raise ValueError("max_results must be between 1 and 20")
    observed={x.strip().lower() for x in symptoms if x.strip()}
    if not observed: raise ValueError("at least one non-empty symptom is required")
    results=[]; seen=set()
    for p in procedures:
        if not p.procedure_id or not p.title or p.procedure_id in seen: raise ValueError("procedure IDs and titles must be unique and non-empty")
        seen.add(p.procedure_id)
        tags={x.lower() for x in p.symptom_tags}
        matched=sorted(observed & tags)
        if matched: results.append({"procedure_id":p.procedure_id,"title":p.title,"matched_symptoms":matched,"prerequisites":list(p.prerequisites),"risk":p.risk,"requires_approval":True,"execute_automatically":False})
    return sorted(results,key=lambda x:(-len(x["matched_symptoms"]),x["risk"],x["procedure_id"]))[:max_results]

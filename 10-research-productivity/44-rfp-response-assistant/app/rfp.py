"""Map RFP requirements to caller-provided approved evidence."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Requirement:
    id:str; question:str
@dataclass(frozen=True)
class Evidence:
    requirement_id:str; approved_text:str; source:str
def map_rfp(requirements:list[Requirement],evidence:list[Evidence])->dict:
    if not requirements: raise ValueError("at least one requirement is required")
    ids=set()
    for req in requirements:
        if not req.id.strip() or not req.question.strip() or req.id in ids: raise ValueError("requirements need unique non-empty ids and questions")
        ids.add(req.id)
    mapped={}
    for item in evidence:
        if item.requirement_id not in ids: raise ValueError(f"evidence references unknown requirement: {item.requirement_id}")
        if not item.approved_text.strip() or not item.source.strip(): raise ValueError("evidence text and source are required")
        mapped.setdefault(item.requirement_id,[]).append({"text":item.approved_text,"source":item.source})
    rows=[{"id":r.id,"question":r.question,"evidence":mapped.get(r.id,[]),"status":"needs_review" if mapped.get(r.id) else "unanswered"} for r in requirements]
    return {"responses":rows,"unanswered_count":sum(r["status"]=="unanswered" for r in rows),"approval_required":True}

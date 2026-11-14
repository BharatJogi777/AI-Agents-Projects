"""Assemble a proposal draft from explicitly supplied facts."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ProposalInput:
    client:str; objective:str; scope:tuple[str,...]; deliverables:tuple[str,...]; milestones:tuple[str,...]; assumptions:tuple[str,...]=()
def draft_proposal(data:ProposalInput)->dict:
    if not data.client.strip() or not data.objective.strip(): raise ValueError("client and objective are required")
    for field,values in (("scope",data.scope),("deliverables",data.deliverables),("milestones",data.milestones)):
        if not values or any(not v.strip() for v in values): raise ValueError(f"{field} must contain non-empty entries")
    if any(not v.strip() for v in data.assumptions): raise ValueError("assumptions cannot contain empty entries")
    return {"title":f"Proposal for {data.client.strip()}","objective":data.objective.strip(),"scope":list(data.scope),"deliverables":list(data.deliverables),"milestones":list(data.milestones),"assumptions":list(data.assumptions),"status":"Draft - requires human review"}

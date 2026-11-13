from dataclasses import dataclass
@dataclass(frozen=True)
class CandidateEvidence:
    candidate_id: str
    skills: tuple[str,...]
    evidence: dict[str,str]
def compare(required_skills: list[str], candidate: CandidateEvidence) -> dict:
    if not candidate.candidate_id.strip(): raise ValueError("candidate_id is required")
    required={s.strip().casefold() for s in required_skills if s.strip()}
    if not required: raise ValueError("at least one required skill is needed")
    supplied={s.strip().casefold() for s in candidate.skills if s.strip()}
    matched=sorted(required & supplied); missing=sorted(required-supplied)
    evidence={k:v for k,v in candidate.evidence.items() if k.casefold() in matched and v.strip()}
    return {"candidate_id":candidate.candidate_id,"matched_job_skills":matched,"not_demonstrated":missing,"evidence":evidence,"protected_attributes_used":False,"candidate_rank":None,"hiring_decision":"human_review_required"}

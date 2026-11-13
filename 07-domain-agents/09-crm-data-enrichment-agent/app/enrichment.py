"""Validate proposed CRM enrichment; never writes to a CRM."""
from dataclasses import dataclass

@dataclass(frozen=True)
class EnrichmentProposal:
    field: str
    current_value: str|None
    proposed_value: str
    source: str
    confidence: float
    action: str

def propose_enrichment(*, field: str, current_value: str|None, proposed_value: str, source: str, confidence: float) -> EnrichmentProposal:
    allowed={"company_name","website","industry","company_size","job_title","business_email","phone"}
    if field not in allowed: raise ValueError(f"field must be one of {sorted(allowed)}")
    if current_value is not None and not isinstance(current_value,str): raise ValueError("current_value must be a string or None")
    for name,value in (("proposed_value",proposed_value),("source",source)):
        if not isinstance(value,str) or not value.strip(): raise ValueError(f"{name} is required")
    if isinstance(confidence,bool) or not isinstance(confidence,(int,float)) or not 0<=confidence<=1: raise ValueError("confidence must be between 0 and 1")
    if current_value and current_value.strip().casefold()==proposed_value.strip().casefold(): action="no_change"
    elif current_value and confidence<0.9: action="manual_review_conflict"
    elif confidence<0.7: action="manual_review_low_confidence"
    else: action="propose_update"
    return EnrichmentProposal(field,current_value,proposed_value.strip(),source.strip(),float(confidence),action)

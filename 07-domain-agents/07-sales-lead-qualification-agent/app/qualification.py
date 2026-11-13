"""Explainable lead qualification from supplied CRM facts."""
from dataclasses import dataclass

@dataclass(frozen=True)
class LeadScore:
    score: int
    band: str
    evidence: tuple[str,...]
    missing_fields: tuple[str,...]

def qualify_lead(*, company_fit: int|None, need: int|None, authority: int|None, timing: int|None, budget_confirmed: bool|None=None) -> LeadScore:
    fields={"company_fit":company_fit,"need":need,"authority":authority,"timing":timing}
    for name,value in fields.items():
        if value is not None and (isinstance(value,bool) or not isinstance(value,int) or not 0<=value<=5): raise ValueError(f"{name} must be an integer from 0 to 5")
    if budget_confirmed is not None and not isinstance(budget_confirmed,bool): raise ValueError("budget_confirmed must be boolean or None")
    missing=tuple(k for k,v in fields.items() if v is None)
    if budget_confirmed is None: missing+=("budget_confirmed",)
    score=sum(v or 0 for v in fields.values())
    if budget_confirmed is True: score+=2
    band="high" if not missing and score>=16 else "medium" if score>=9 else "low"
    evidence=tuple(f"{k.replace('_',' ').title()}: {v}/5" for k,v in fields.items() if v is not None)
    if budget_confirmed is not None: evidence+=(f"Budget confirmed: {'yes' if budget_confirmed else 'no'}",)
    if missing: evidence+=("Score is provisional because evidence is missing.",)
    return LeadScore(score,band,evidence,missing)

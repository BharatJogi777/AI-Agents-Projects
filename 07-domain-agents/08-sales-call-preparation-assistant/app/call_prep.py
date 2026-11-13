"""Prepare a sales call brief without fabricating prospect research."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CallBrief:
    objective: str
    agenda: tuple[str,...]
    known_context: tuple[str,...]
    questions: tuple[str,...]

def prepare_call(*, account_name: str, objective: str, context: list[str], stakeholders: list[str], open_questions: list[str]) -> CallBrief:
    if not isinstance(account_name,str) or not account_name.strip() or not isinstance(objective,str) or not objective.strip(): raise ValueError("account_name and objective are required")
    for name,values in (("context",context),("stakeholders",stakeholders),("open_questions",open_questions)):
        if not isinstance(values,list) or any(not isinstance(v,str) or not v.strip() for v in values): raise ValueError(f"{name} must be a list of non-empty strings")
    agenda=["Confirm attendees, roles and meeting objective","Validate the prospect's current situation and desired outcome","Explore impact, constraints, decision process and timeline","Agree on owners and specific next steps"]
    if stakeholders: agenda.insert(1,"Confirm stakeholder priorities: "+", ".join(stakeholders))
    return CallBrief(objective.strip(),tuple(agenda),tuple(context),tuple(open_questions))

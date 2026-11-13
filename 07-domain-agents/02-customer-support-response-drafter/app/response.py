"""Draft support responses using only supplied, verified case facts."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ResponseDraft:
    subject: str
    body: str
    included_facts: tuple[str,...]
    requires_agent_review: bool=True

def draft_response(customer_name: str, issue: str, verified_facts: list[str], next_steps: list[str], *, policy_text: str | None=None) -> ResponseDraft:
    if not isinstance(customer_name,str) or not customer_name.strip() or not isinstance(issue,str) or not issue.strip(): raise ValueError("customer_name and issue are required")
    for name,items in (("verified_facts",verified_facts),("next_steps",next_steps)):
        if not isinstance(items,list) or any(not isinstance(x,str) or not x.strip() for x in items): raise ValueError(f"{name} must contain non-empty strings")
    if policy_text is not None and (not isinstance(policy_text,str) or not policy_text.strip()): raise ValueError("policy_text must be non-empty when supplied")
    lines=[f"Hello {customer_name.strip()},","",f"Thank you for contacting us about: {issue.strip()}.",""]
    if verified_facts:
        lines.append("What we have confirmed:"); lines.extend(f"- {x}" for x in verified_facts); lines.append("")
    if policy_text: lines.extend(["Relevant policy information:",policy_text.strip(),""])
    if next_steps:
        lines.append("Next steps:"); lines.extend(f"- {x}" for x in next_steps); lines.append("")
    lines.append("If anything above does not match your experience, please reply so our team can review it.")
    return ResponseDraft(f"Update on your support request", "\n".join(lines),tuple(verified_facts))

"""Prepare a reply draft that requires explicit human approval before sending."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReplyDraft:
    recipient: str
    subject: str
    body: str
    requires_approval: bool = True
    approved: bool = False

def draft_reply(*, recipient: str, subject: str, key_points: list[str], tone: str = "professional") -> ReplyDraft:
    if not isinstance(recipient,str) or "@" not in recipient: raise ValueError("recipient must be a valid-looking email address")
    if not isinstance(subject,str) or not subject.strip(): raise ValueError("subject must be non-empty")
    if not isinstance(key_points,list) or any(not isinstance(x,str) or not x.strip() for x in key_points): raise ValueError("key_points must be non-empty strings")
    if tone not in ("professional","friendly","concise"): raise ValueError("unsupported tone")
    greeting="Hello,"
    closing={"professional":"Best regards,","friendly":"Thanks,","concise":"Regards,"}[tone]
    body="\n".join([greeting,"",*("- "+p.strip() for p in key_points),"",closing])
    return ReplyDraft(recipient.strip(),subject.strip(),body)

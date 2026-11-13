"""Create validated email drafts without sending or addressing recipients."""
from dataclasses import dataclass
import re

_EMAIL=re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
@dataclass(frozen=True)
class EmailDraft:
    subject:str
    body:str
    recipients:tuple[str,...]

def create_draft(subject:str,body:str,recipients:list[str])->EmailDraft:
    if not subject.strip() or len(subject)>200: raise ValueError("subject is required and must be <= 200 characters")
    if not body.strip() or len(body)>20_000: raise ValueError("body is required and must be <= 20000 characters")
    if len(recipients)>20 or any(not _EMAIL.fullmatch(address) for address in recipients):
        raise ValueError("recipient list contains invalid address or exceeds limit")
    if len(set(a.casefold() for a in recipients))!=len(recipients): raise ValueError("duplicate recipients")
    return EmailDraft(subject.strip(),body.strip(),tuple(recipients))

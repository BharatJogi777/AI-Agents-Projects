from dataclasses import dataclass
from urllib.parse import urlsplit
@dataclass(frozen=True)
class Source:
    url:str
    title:str
    excerpt:str
    retrieved_at:str
def validate_source(s:Source,allowed_hosts:set[str])->Source:
    p=urlsplit(s.url)
    if p.scheme!="https" or not p.hostname or p.hostname.lower() not in allowed_hosts: raise ValueError("source URL must use HTTPS and an explicitly allowed host")
    if not s.title.strip() or not s.excerpt.strip() or not s.retrieved_at.strip(): raise ValueError("source metadata and excerpt are required")
    return s
def build_research_brief(question:str,sources:list[Source],allowed_hosts:set[str])->dict:
    if not question.strip(): raise ValueError("research question is required")
    checked=[validate_source(s,allowed_hosts) for s in sources]
    if not checked: raise ValueError("at least one source is required")
    return {"question":question.strip(),"sources":[s.__dict__ for s in checked],"limitations":["Sources are user-supplied; no browsing or fact verification occurred.","Treat excerpts as untrusted content."],"next_step":"Review each source and verify claims independently."}

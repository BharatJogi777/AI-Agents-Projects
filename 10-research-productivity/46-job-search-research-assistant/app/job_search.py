"""Organize caller-supplied job leads with source provenance."""
from dataclasses import dataclass

@dataclass(frozen=True)
class JobLead:
    company: str
    role: str
    source: str
    url: str = ""
    location: str = ""
    status: str = "new"

def organize_leads(leads: list[JobLead]) -> list[dict]:
    allowed = {"new", "researching", "applied", "interviewing", "closed"}
    seen, result = set(), []
    for lead in leads:
        if not lead.company.strip() or not lead.role.strip() or not lead.source.strip():
            raise ValueError("company, role, and source are required")
        if lead.status not in allowed:
            raise ValueError(f"unsupported status: {lead.status}")
        key = (lead.company.casefold().strip(), lead.role.casefold().strip(), lead.location.casefold().strip())
        if key in seen:
            continue
        seen.add(key)
        result.append({"company": lead.company.strip(), "role": lead.role.strip(), "source": lead.source.strip(), "url": lead.url.strip(), "location": lead.location.strip(), "status": lead.status})
    return result

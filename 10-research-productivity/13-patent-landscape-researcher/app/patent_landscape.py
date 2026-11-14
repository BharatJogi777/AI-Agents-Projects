"""Summarize a caller-supplied patent set by status and technology area."""
from dataclasses import dataclass
@dataclass(frozen=True)
class PatentLandscape:
    total_records: int
    status_counts: tuple[tuple[str,int],...]
    technology_counts: tuple[tuple[str,int],...]
    records_missing_dates: tuple[str,...]
def summarize_patents(*, records: list[dict]) -> PatentLandscape:
    if not isinstance(records,list): raise ValueError("records must be a list")
    statuses={}; technologies={}; missing=[]; seen=set()
    for row in records:
        if not isinstance(row,dict): raise ValueError("each record must be a dictionary")
        for key in ("patent_id","status","technology"):
            if not isinstance(row.get(key),str) or not row[key].strip(): raise ValueError(f"{key} must be non-empty")
        pid=row["patent_id"].strip()
        if pid in seen: raise ValueError("patent_id values must be unique")
        seen.add(pid)
        status=row["status"].strip().casefold(); tech=row["technology"].strip()
        statuses[status]=statuses.get(status,0)+1; technologies[tech]=technologies.get(tech,0)+1
        if not isinstance(row.get("filing_date",""),str) or not row.get("filing_date","").strip(): missing.append(pid)
    return PatentLandscape(len(records),tuple(sorted(statuses.items())),tuple(sorted(technologies.items())),tuple(missing))

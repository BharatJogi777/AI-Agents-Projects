"""Turn stakeholder notes into traceable product requirements."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    statement: str
    source: str
    priority: str
    acceptance_criteria: tuple[str, ...]

def analyze_requirements(*, needs: list[dict]) -> list[Requirement]:
    """Validate and normalize supplied needs; never invent missing stakeholder intent."""
    if not isinstance(needs, list):
        raise TypeError("needs must be a list")
    results = []
    seen = set()
    for index, item in enumerate(needs, 1):
        if not isinstance(item, dict):
            raise TypeError(f"need {index} must be a dictionary")
        statement = item.get("statement")
        source = item.get("source")
        if not isinstance(statement, str) or not statement.strip():
            raise ValueError(f"need {index} requires a non-empty statement")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"need {index} requires a source")
        rid = str(item.get("id") or f"REQ-{index:03d}").strip()
        if not rid or rid in seen:
            raise ValueError(f"duplicate or empty requirement id: {rid}")
        seen.add(rid)
        priority = str(item.get("priority", "medium")).lower()
        if priority not in {"low", "medium", "high", "critical"}:
            raise ValueError(f"invalid priority for {rid}")
        criteria = item.get("acceptance_criteria", [])
        if not isinstance(criteria, list) or any(not isinstance(x, str) or not x.strip() for x in criteria):
            raise ValueError(f"acceptance_criteria for {rid} must be a list of non-empty strings")
        results.append(Requirement(rid, statement.strip(), source.strip(), priority, tuple(x.strip() for x in criteria)))
    return results

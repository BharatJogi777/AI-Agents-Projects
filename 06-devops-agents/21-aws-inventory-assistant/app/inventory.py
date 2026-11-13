"""Read-only inventory analysis for exported AWS resource snapshots."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Finding:
    resource_id: str
    resource_type: str
    severity: str
    reason: str

def analyze_inventory(resources: list[dict[str, Any]]) -> list[Finding]:
    if not isinstance(resources, list):
        raise TypeError("resources must be a list")
    findings: list[Finding] = []
    seen: set[tuple[str, str]] = set()
    for index, item in enumerate(resources):
        if not isinstance(item, dict):
            raise ValueError(f"resource at index {index} must be an object")
        rid, kind = item.get("id"), item.get("type")
        if not isinstance(rid, str) or not rid.strip() or not isinstance(kind, str) or not kind.strip():
            raise ValueError(f"resource at index {index} requires non-empty id and type")
        key = (kind, rid)
        if key in seen:
            raise ValueError(f"duplicate resource: {kind}/{rid}")
        seen.add(key)
        state = str(item.get("state", "")).lower()
        public = item.get("public", False)
        attached = item.get("attached", True)
        if not isinstance(public, bool) or not isinstance(attached, bool):
            raise ValueError(f"resource {rid}: public and attached must be booleans")
        if public:
            findings.append(Finding(rid, kind, "high", "Resource is marked publicly accessible; verify intended exposure."))
        if kind in {"ebs-volume", "elastic-ip", "load-balancer"} and not attached:
            findings.append(Finding(rid, kind, "medium", "Resource is unattached; verify ownership before cleanup."))
        if state in {"failed", "degraded", "unavailable"}:
            findings.append(Finding(rid, kind, "high", f"Reported resource state is {state}."))
    return findings

"""Detect tenant-boundary violations in retrieved memory metadata."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Memory:
    memory_id: str
    tenant_id: str
    content: str

@dataclass(frozen=True)
class LeakageFinding:
    memory_id: str
    reason: str

def audit_memory_retrieval(tenant_id: str, memories: list[Memory]) -> tuple[LeakageFinding, ...]:
    if not isinstance(tenant_id, str) or not tenant_id.strip():
        raise ValueError("tenant_id is required")
    findings = []
    for item in memories:
        if not item.memory_id or not item.tenant_id:
            findings.append(LeakageFinding(item.memory_id or "<unknown>", "missing ownership metadata"))
        elif item.tenant_id != tenant_id:
            findings.append(LeakageFinding(item.memory_id, "tenant mismatch"))
    return tuple(findings)

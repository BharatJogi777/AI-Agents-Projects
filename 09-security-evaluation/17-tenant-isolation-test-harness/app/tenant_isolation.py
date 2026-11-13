"""Validate tenant ownership at a repository boundary."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Record:
    record_id: str
    tenant_id: str
    payload: str = ""

@dataclass(frozen=True)
class IsolationReport:
    passed: bool
    leaked_record_ids: tuple[str, ...]

def check_isolation(requested_tenant: str, records: list[Record]) -> IsolationReport:
    if not isinstance(requested_tenant, str) or not requested_tenant.strip():
        raise ValueError("requested_tenant is required")
    if any(not r.tenant_id for r in records):
        raise ValueError("every record must have a tenant_id")
    leaked = tuple(sorted(r.record_id for r in records if r.tenant_id != requested_tenant))
    return IsolationReport(not leaked, leaked)

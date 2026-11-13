"""Dependency-free distributed trace diagnostics."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Span:
    span_id: str
    name: str
    start_ms: float
    end_ms: float
    parent_id: str | None = None
    status: str = "ok"

def investigate_trace(spans: list[Span], *, slow_ms: float = 500.0) -> dict:
    if slow_ms < 0: raise ValueError("slow_ms must be non-negative")
    ids=[s.span_id for s in spans]
    if any(not x for x in ids) or len(ids)!=len(set(ids)): raise ValueError("span IDs must be non-empty and unique")
    known=set(ids); findings=[]
    for s in spans:
        if s.end_ms < s.start_ms: raise ValueError(f"span {s.span_id} ends before it starts")
        if s.parent_id and s.parent_id not in known: findings.append({"span_id":s.span_id,"kind":"missing-parent","duration_ms":s.end_ms-s.start_ms})
        if s.status.lower() not in {"ok","success"}: findings.append({"span_id":s.span_id,"kind":"error","duration_ms":s.end_ms-s.start_ms})
        if s.end_ms-s.start_ms >= slow_ms: findings.append({"span_id":s.span_id,"kind":"slow","duration_ms":s.end_ms-s.start_ms})
    return {"duration_ms":max((s.end_ms for s in spans),default=0)-min((s.start_ms for s in spans),default=0),"findings":sorted(findings,key=lambda x:(x["span_id"],x["kind"]))}

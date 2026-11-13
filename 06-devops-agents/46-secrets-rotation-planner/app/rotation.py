"""Plan secret rotation from metadata only; never handle secret material."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RotationStep:
    secret_id: str
    owner: str
    dependents: tuple[str,...]
    sequence: int
    requires_approval: bool=True

def plan_rotation(records: list[dict]) -> list[RotationStep]:
    if not isinstance(records,list): raise TypeError("records must be a list")
    by_id={}
    for i,r in enumerate(records):
        if not isinstance(r,dict): raise ValueError(f"record {i} must be an object")
        sid=r.get("secret_id"); owner=r.get("owner"); deps=r.get("dependents",[])
        if not isinstance(sid,str) or not sid.strip() or sid in by_id: raise ValueError("secret_id must be unique and non-empty")
        if not isinstance(owner,str) or not owner.strip(): raise ValueError(f"{sid}: owner is required")
        if not isinstance(deps,list) or any(not isinstance(x,str) or not x for x in deps): raise ValueError(f"{sid}: dependents must be names")
        by_id[sid]=(owner,deps)
    # Edges from a secret to its consumers; rotate leaves first so consumers can be coordinated afterwards.
    visiting=set(); visited=set(); ordered=[]
    def visit(sid):
        if sid in visiting: raise ValueError("dependency cycle detected")
        if sid in visited: return
        visiting.add(sid)
        for dep in by_id[sid][1]:
            if dep in by_id: visit(dep)
        visiting.remove(sid); visited.add(sid); ordered.append(sid)
    for sid in sorted(by_id): visit(sid)
    return [RotationStep(sid,by_id[sid][0],tuple(sorted(by_id[sid][1])),i+1) for i,sid in enumerate(ordered)]

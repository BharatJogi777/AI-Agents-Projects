"""Deterministic monorepo impact analysis from a declared component manifest."""
from dataclasses import dataclass
from pathlib import PurePosixPath

@dataclass(frozen=True)
class Component:
    name: str
    paths: tuple[str, ...]
    depends_on: tuple[str, ...] = ()

def analyze_impact(changed_paths: list[str], components: list[Component]) -> dict[str, list[str]]:
    names = {c.name for c in components}
    if len(names) != len(components): raise ValueError("component names must be unique")
    for c in components:
        if not c.name or any(d not in names for d in c.depends_on):
            raise ValueError(f"invalid component or dependency: {c.name}")
    changed = [str(PurePosixPath(p)) for p in changed_paths]
    if any(p.startswith("/") or ".." in PurePosixPath(p).parts for p in changed):
        raise ValueError("changed paths must be safe repository-relative paths")
    direct = {c.name: [p for p in changed if any(p == prefix.rstrip("/") or p.startswith(prefix.rstrip("/") + "/") for prefix in c.paths)] for c in components}
    affected = {name for name, paths in direct.items() if paths}
    reverse = {c.name: set() for c in components}
    for c in components:
        for dep in c.depends_on: reverse[dep].add(c.name)
    queue = list(affected)
    while queue:
        current = queue.pop(0)
        for consumer in sorted(reverse[current]):
            if consumer not in affected: affected.add(consumer); queue.append(consumer)
    return {"direct": sorted(k for k,v in direct.items() if v), "affected": sorted(affected), "unmapped": sorted(p for p in changed if not any(p in paths for paths in direct.values()))}

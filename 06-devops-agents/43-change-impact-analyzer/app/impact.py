"""Assess downstream blast radius from a directed dependency map."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ImpactReport:
    changed_components: tuple[str,...]
    affected_services: tuple[str,...]
    risk: str

def analyze_change_impact(graph: dict[str,list[str]], changed: list[str]) -> ImpactReport:
    if not isinstance(graph,dict) or not isinstance(changed,list) or not changed: raise ValueError("graph must be an object and changed must be a non-empty list")
    nodes=set(graph)
    for source,targets in graph.items():
        if not isinstance(source,str) or not source or not isinstance(targets,list) or any(not isinstance(t,str) or not t for t in targets): raise ValueError("graph must map names to lists of names")
        nodes.update(targets)
    if any(not isinstance(x,str) or x not in nodes for x in changed): raise ValueError("every changed component must exist in the dependency graph")
    affected=set(); stack=list(changed); visited=set(changed)
    reverse={n:[] for n in nodes}
    for source,targets in graph.items():
        for target in targets: reverse[target].append(source)
    while stack:
        node=stack.pop()
        for dependent in reverse[node]:
            if dependent not in visited: visited.add(dependent); affected.add(dependent); stack.append(dependent)
    affected.difference_update(changed); risk="high" if len(affected)>=10 else "medium" if len(affected)>=4 else "low"
    return ImpactReport(tuple(sorted(set(changed))),tuple(sorted(affected)),risk)

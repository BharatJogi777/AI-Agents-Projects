"""Build and inspect a directed service dependency graph."""
from collections import defaultdict, deque
from dataclasses import dataclass

@dataclass(frozen=True)
class DependencyReport:
    services: tuple[str,...]
    edges: tuple[tuple[str,str],...]
    cycles: tuple[tuple[str,...],...]

def build_dependency_map(edges: list[tuple[str,str]]) -> DependencyReport:
    if not isinstance(edges,list): raise TypeError("edges must be a list")
    graph=defaultdict(list); nodes=set(); normalized=[]; seen=set()
    for i,edge in enumerate(edges):
        if not isinstance(edge,(tuple,list)) or len(edge)!=2: raise ValueError(f"edge {i} must contain source and target")
        source,target=edge
        if not isinstance(source,str) or not source.strip() or not isinstance(target,str) or not target.strip(): raise ValueError(f"edge {i} contains invalid service name")
        if source==target: raise ValueError(f"self dependency is not allowed: {source}")
        if (source,target) in seen: continue
        seen.add((source,target)); normalized.append((source,target)); graph[source].append(target); nodes.update((source,target))
    state={}; stack=[]; cycles=[]
    def visit(node):
        state[node]=1; stack.append(node)
        for nxt in graph[node]:
            if state.get(nxt,0)==0: visit(nxt)
            elif state.get(nxt)==1:
                start=stack.index(nxt); cycle=tuple(stack[start:]+[nxt])
                if cycle not in cycles: cycles.append(cycle)
        stack.pop(); state[node]=2
    for node in sorted(nodes):
        if state.get(node,0)==0: visit(node)
    return DependencyReport(tuple(sorted(nodes)),tuple(sorted(normalized)),tuple(cycles))

def downstream(report: DependencyReport, service: str) -> set[str]:
    graph=defaultdict(list)
    for source,target in report.edges: graph[source].append(target)
    found=set(); queue=deque(graph[service])
    while queue:
        node=queue.popleft()
        if node in found or node==service: continue
        found.add(node); queue.extend(graph[node])
    return found

def upstream(report: DependencyReport, service: str) -> set[str]:
    reverse=defaultdict(list)
    for source,target in report.edges: reverse[target].append(source)
    found=set(); queue=deque(reverse[service])
    while queue:
        node=queue.popleft()
        if node in found or node==service: continue
        found.add(node); queue.extend(reverse[node])
    return found

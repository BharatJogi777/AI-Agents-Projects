"""Analyze a caller-provided citation graph using deterministic graph traversal."""
from dataclasses import dataclass
@dataclass(frozen=True)
class CitationNetwork:
    nodes: tuple[str,...]
    edges: tuple[tuple[str,str],...]
    orphan_nodes: tuple[str,...]
    unknown_references: tuple[tuple[str,str],...]
def analyze_citations(*, papers: list[str], citations: dict[str,list[str]]) -> CitationNetwork:
    if not isinstance(papers,list) or any(not isinstance(p,str) or not p.strip() for p in papers): raise ValueError("papers must be a list of non-empty IDs")
    if len(set(papers))!=len(papers): raise ValueError("paper IDs must be unique")
    if not isinstance(citations,dict): raise ValueError("citations must be a dictionary")
    known=set(papers); edges=[]; unknown=[]; cited=set()
    for source, targets in citations.items():
        if source not in known or not isinstance(targets,list) or any(not isinstance(t,str) or not t.strip() for t in targets): raise ValueError("citation entries need known source IDs and lists of target IDs")
        for target in targets:
            if target in known: edges.append((source,target)); cited.add(target)
            else: unknown.append((source,target))
    outgoing={s for s,_ in edges}
    orphans=tuple(sorted(known-(outgoing|cited)))
    return CitationNetwork(tuple(papers),tuple(edges),orphans,tuple(unknown))

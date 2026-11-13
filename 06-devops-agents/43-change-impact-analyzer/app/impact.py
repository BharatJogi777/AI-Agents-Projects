from dataclasses import dataclass
@dataclass(frozen=True)
class ImpactReport:
 changed_component:str
 affected_components:tuple[str,...]
 impact_count:int
 circular_dependencies:tuple[str,...]
def analyze_impact(graph:dict[str,list[str]],changed:str)->ImpactReport:
 if not isinstance(graph,dict) or not isinstance(changed,str) or not changed.strip(): raise ValueError('graph and changed component required')
 if changed not in graph: raise ValueError('changed component must be a graph key')
 for node,edges in graph.items():
  if not isinstance(node,str) or not node.strip() or not isinstance(edges,list) or any(not isinstance(x,str) or not x.strip() for x in edges): raise ValueError('invalid graph structure')
 unknown={x for edges in graph.values() for x in edges if x not in graph}
 if unknown: raise ValueError(f'unknown nodes: {sorted(unknown)}')
 reverse={n:set() for n in graph}
 for src,targets in graph.items():
  for target in targets: reverse[target].add(src)
 seen=set(); stack=list(reverse[changed])
 while stack:
  n=stack.pop()
  if n in seen: continue
  seen.add(n); stack.extend(reverse[n]-seen)
 cycles=tuple(sorted(n for n in seen if n in graph[n] or (changed in graph[n] and n in reverse[changed])))
 return ImpactReport(changed,tuple(sorted(seen)),len(seen),cycles)

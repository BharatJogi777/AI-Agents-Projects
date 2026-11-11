from dataclasses import dataclass
from collections import deque
from collections.abc import Iterable
@dataclass(frozen=True)
class Edge: source:str; relation:str; target:str; evidence_id:str
@dataclass(frozen=True)
class GraphPath: nodes:tuple[str,...]; relations:tuple[str,...]; evidence_ids:tuple[str,...]
def find_paths(start:str,target:str,edges:Iterable[Edge],max_hops:int=3,max_paths:int=20)->list[GraphPath]:
 if not start or not target or not 1<=max_hops<=8 or max_paths<1: raise ValueError("invalid traversal parameters")
 graph={}
 for e in edges:
  if not all((e.source,e.relation,e.target,e.evidence_id)): raise ValueError("edge fields required")
  graph.setdefault(e.source,[]).append(e)
 queue=deque([(start,(start,),(),())]); found=[]
 while queue and len(found)<max_paths:
  node,nodes,rels,proof=queue.popleft()
  if node==target and len(rels)>0: found.append(GraphPath(nodes,rels,proof)); continue
  if len(rels)>=max_hops: continue
  for e in sorted(graph.get(node,[]),key=lambda x:(x.target,x.relation,x.evidence_id)):
   if e.target not in nodes: queue.append((e.target,nodes+(e.target,),rels+(e.relation,),proof+(e.evidence_id,)))
 return found

from dataclasses import dataclass
from collections.abc import Callable,Sequence
@dataclass(frozen=True)
class Passage: id:str; text:str; metadata:dict
@dataclass(frozen=True)
class RankedPassage: passage:Passage; relevance:float; original_rank:int
def rerank(query:str,candidates:Sequence[Passage],scorer:Callable[[str,str],float],limit:int=5)->list[RankedPassage]:
 if not query.strip() or limit<1: raise ValueError("query and positive limit required")
 seen=set(); ranked=[]
 for rank,p in enumerate(candidates,1):
  if not p.id or p.id in seen: continue
  seen.add(p.id); score=scorer(query,p.text)
  if isinstance(score,bool) or not isinstance(score,(int,float)) or not -1<=score<=1: raise ValueError("scorer must return a finite relevance score in [-1, 1]")
  ranked.append(RankedPassage(p,float(score),rank))
 ranked.sort(key=lambda x:(-x.relevance,x.original_rank,x.passage.id))
 return ranked[:limit]

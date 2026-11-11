from dataclasses import dataclass
@dataclass(frozen=True)
class SearchHit: id:str; score:float; source:str
@dataclass(frozen=True)
class FusedHit: id:str; score:float; ranks:dict[str,int]
def reciprocal_rank_fusion(rankings,k=60,limit=10):
 if k<1 or limit<1: raise ValueError("k and limit must be positive")
 scores={}; ranks={}
 for source,hits in rankings.items():
  seen=set()
  for rank,hit in enumerate(hits,1):
   if hit.id in seen: continue
   seen.add(hit.id); scores[hit.id]=scores.get(hit.id,0)+1/(k+rank); ranks.setdefault(hit.id,{})[source]=rank
 return [FusedHit(i,scores[i],ranks[i]) for i in sorted(scores,key=lambda x:(-scores[x],x))[:limit]]

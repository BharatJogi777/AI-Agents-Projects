from dataclasses import dataclass
@dataclass(frozen=True)
class Candidate: id:str; payload:object; score:float
@dataclass(frozen=True)
class MultiQueryResult: id:str; payload:object; score:float; matched_queries:tuple[int,...]
def multi_query_retrieve(queries,search,limit=10,k=60):
 if not queries or limit<1 or k<1: raise ValueError("queries, positive limit and k required")
 scores={}; payloads={}; matched={}
 for qi,q in enumerate(queries):
  for rank,c in enumerate(search(q),1):
   if c.id not in scores: scores[c.id]=0; payloads[c.id]=c.payload; matched[c.id]=[]
   scores[c.id]+=1/(k+rank)
   if qi not in matched[c.id]: matched[c.id].append(qi)
 return [MultiQueryResult(i,payloads[i],scores[i],tuple(matched[i])) for i in sorted(scores,key=lambda x:(-scores[x],x))[:limit]]

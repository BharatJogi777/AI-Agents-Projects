from dataclasses import dataclass
@dataclass(frozen=True)
class Memory:id:str;text:str;confirmed:bool;confidence:float;created_at:float;expires_at:float|None=None;sensitive:bool=False
def retrieve(query,memories,now,limit=5,min_confidence=.5):
 if not query.strip() or limit<1:raise ValueError("query and positive limit required")
 terms=set(query.lower().split());ranked=[]
 for m in memories:
  if not m.confirmed or m.sensitive or m.confidence<min_confidence or (m.expires_at is not None and m.expires_at<=now):continue
  overlap=len(terms & set(m.text.lower().split()))/max(1,len(terms))
  if overlap:
   recency=1/(1+max(0,now-m.created_at)/86400)
   ranked.append((.65*overlap+.25*m.confidence+.1*recency,m.created_at,m.id,m))
 ranked.sort(key=lambda x:(-x[0],-x[1],x[2]));return [x[3] for x in ranked[:limit]]

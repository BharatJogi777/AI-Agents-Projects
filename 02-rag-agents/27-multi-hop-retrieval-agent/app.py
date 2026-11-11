from dataclasses import dataclass
from collections.abc import Callable,Sequence
@dataclass(frozen=True)
class HopEvidence: source_id:str; text:str
@dataclass(frozen=True)
class HopResult: hop:int; query:str; evidence:tuple[HopEvidence,...]
def multi_hop_retrieve(question:str,retrieve:Callable[[str],Sequence[HopEvidence]],derive_next:Callable[[str,Sequence[HopEvidence]],str],max_hops:int=3)->list[HopResult]:
 if not question.strip() or not 1<=max_hops<=5: raise ValueError("question and max_hops 1..5 required")
 query=question; results=[]; seen=set()
 for hop in range(1,max_hops+1):
  found=[]
  for item in retrieve(query):
   if not item.source_id or not item.text.strip(): continue
   if item.source_id not in seen: found.append(item); seen.add(item.source_id)
  results.append(HopResult(hop,query,tuple(found)))
  if not found: break
  if hop<max_hops:
   next_query=derive_next(question,found)
   if not isinstance(next_query,str) or not next_query.strip(): break
   query=next_query.strip()[:1000]
 return results

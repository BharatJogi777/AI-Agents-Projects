from dataclasses import dataclass
from collections.abc import Iterable
@dataclass(frozen=True)
class Triple: subject:str; predicate:str; object:str; source_id:str
def validate_triples(triples:Iterable[Triple],allowed_predicates:set[str],max_items:int=10000)->list[Triple]:
 out=[]; seen=set()
 for t in triples:
  if len(out)>=max_items: raise ValueError("triple limit exceeded")
  if not all(isinstance(x,str) and x.strip() for x in (t.subject,t.predicate,t.object,t.source_id)): raise ValueError("triple fields must be non-empty strings")
  if t.predicate not in allowed_predicates: raise ValueError("predicate not allowed")
  key=(t.subject,t.predicate,t.object,t.source_id)
  if key not in seen: out.append(t); seen.add(key)
 return out
def retrieve_connected(entity:str,triples:Iterable[Triple],max_results:int=20)->list[Triple]:
 if not entity or max_results<1: raise ValueError("entity and positive result limit required")
 return [t for t in triples if t.subject.casefold()==entity.casefold() or t.object.casefold()==entity.casefold()][:max_results]

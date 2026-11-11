from dataclasses import dataclass
import re
from collections.abc import Callable,Sequence
@dataclass(frozen=True)
class Evidence: document_id:str; text:str
@dataclass(frozen=True)
class CompressedSpan: document_id:str; start:int; end:int; text:str; score:float
def compress_context(query:str,evidence:Sequence[Evidence],score:Callable[[str,str],float],max_chars:int=3000)->list[CompressedSpan]:
 if not query.strip() or max_chars<1: raise ValueError("query and positive budget required")
 candidates=[]
 for ev in evidence:
  if not ev.document_id: raise ValueError("document ID required")
  for m in re.finditer(r"[^.!?\\n]+(?:[.!?]+|$)",ev.text):
   raw=m.group(); left=len(raw)-len(raw.lstrip()); right=len(raw.rstrip()); start=m.start()+left; end=m.start()+right; sentence=ev.text[start:end]
   if not sentence: continue
   value=score(query,sentence)
   if isinstance(value,bool) or not isinstance(value,(int,float)) or not -1<=value<=1: raise ValueError("score must be in [-1, 1]")
   candidates.append(CompressedSpan(ev.document_id,start,end,sentence,float(value)))
 candidates.sort(key=lambda x:(-x.score,x.document_id,x.start)); chosen=[]; used=0
 for item in candidates:
  cost=len(item.text)+(1 if chosen else 0)
  if used+cost<=max_chars: chosen.append(item); used+=cost
 return sorted(chosen,key=lambda x:(x.document_id,x.start))

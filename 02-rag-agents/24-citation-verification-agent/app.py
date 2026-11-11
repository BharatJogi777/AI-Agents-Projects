from dataclasses import dataclass
from collections.abc import Sequence
@dataclass(frozen=True)
class Citation: source_id:str; quote:str
@dataclass(frozen=True)
class CitationCheck: citation:Citation; valid:bool; reason:str
def verify_citations(citations:Sequence[Citation],sources:dict[str,str])->list[CitationCheck]:
 checks=[]
 for c in citations:
  if not c.source_id or c.source_id not in sources: checks.append(CitationCheck(c,False,"unknown source")); continue
  if not c.quote.strip(): checks.append(CitationCheck(c,False,"empty quote")); continue
  if c.quote not in sources[c.source_id]: checks.append(CitationCheck(c,False,"quote is not an exact source substring")); continue
  checks.append(CitationCheck(c,True,"exact quote found"))
 return checks

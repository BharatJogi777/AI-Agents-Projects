from dataclasses import dataclass
@dataclass(frozen=True)
class HyDEResult: original_query:str; hypothetical_document:str; retrieval_query:str
class HyDEAgent:
 def __init__(self,generator,max_chars=2000): self.generator=generator; self.max_chars=max_chars
 def generate(self,query):
  if not query or len(query)>self.max_chars: raise ValueError("query empty or too long")
  h=self.generator(query)
  if not isinstance(h,str) or not h.strip() or len(h)>self.max_chars: raise ValueError("invalid hypothetical document")
  return HyDEResult(query,h.strip(),h.strip())

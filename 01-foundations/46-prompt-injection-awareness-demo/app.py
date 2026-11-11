"""AG-046: Separate trusted policy from untrusted request and retrieved text."""
from dataclasses import dataclass
@dataclass(frozen=True)
class PromptParts: policy:str; request:str; retrieved:str
class PromptBuilder:
 def __init__(self,max_chars=12000):
  if max_chars<100: raise ValueError("minimum limit is 100")
  self.max_chars=max_chars
 def build(self,p):
  values=(p.policy,p.request,p.retrieved)
  if any(not isinstance(v,str) for v in values): raise TypeError("all sections must be text")
  if sum(map(len,values))>self.max_chars: raise ValueError("prompt too large")
  return f"TRUSTED POLICY:\n{p.policy}\n\nUSER REQUEST (untrusted):\n{p.request}\n\nRETRIEVED DATA (untrusted):\n<untrusted>\n{p.retrieved}\n</untrusted>"
 @staticmethod
 def allowed(action,allowlist,approved=False): return action in allowlist and approved

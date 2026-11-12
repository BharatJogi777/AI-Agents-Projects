import json,re
from dataclasses import dataclass
SENSITIVE={"password","passwd","token","access_token","refresh_token","api_key","apikey","secret","authorization","client_secret"}
class ToolOutputError(ValueError):pass
@dataclass(frozen=True)
class ToolEnvelope:
 tool:str;trust:str;content:str;truncated:bool;original_chars:int
 def __getitem__(self,key):return getattr(self,key)
 def as_dict(self):return {"tool":self.tool,"trust":self.trust,"content":self.content,"truncated":self.truncated,"original_chars":self.original_chars}
class ToolOutputNormalizer:
 def __init__(self,max_chars=4000,max_depth=12):
  if max_chars<32 or max_depth<1:raise ValueError("invalid output limits")
  self.max_chars=max_chars;self.max_depth=max_depth
 def _safe(self,value,depth,seen):
  if depth>self.max_depth:return "[MAX_DEPTH]"
  if value is None or isinstance(value,(str,int,bool)):return value
  if isinstance(value,float):
   if value!=value or value in (float("inf"),float("-inf")):return "[NON_FINITE_NUMBER]"
   return value
  if isinstance(value,dict):
   if id(value) in seen:return "[CIRCULAR_REFERENCE]"
   seen.add(id(value));out={}
   for k,v in list(value.items())[:500]:
    key=str(k);normalized=re.sub(r"[^a-z0-9_]","",key.lower())
    sensitive={re.sub(r"[^a-z0-9_]","",s) for s in SENSITIVE}
    out[key]="[REDACTED]" if normalized in sensitive else self._safe(v,depth+1,seen)
   seen.remove(id(value));return out
  if isinstance(value,(list,tuple)):
   if id(value) in seen:return "[CIRCULAR_REFERENCE]"
   seen.add(id(value));out=[self._safe(v,depth+1,seen) for v in value[:500]];seen.remove(id(value));return out
  return f"[UNSUPPORTED:{type(value).__name__}]"
 def normalize(self,name,value):
  if not isinstance(name,str) or not name.strip() or len(name)>100:raise ToolOutputError("invalid tool name")
  raw=json.dumps(self._safe(value,0,set()),sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False)
  return ToolEnvelope(name,"untrusted",raw[:self.max_chars],len(raw)>self.max_chars,len(raw))

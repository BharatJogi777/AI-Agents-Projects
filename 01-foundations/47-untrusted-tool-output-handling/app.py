"""AG-047: Untrusted tool-output handling. Serialize tool results into bounded, trust-labeled envelopes and redact common credential patterns before model-context insertion."""
import json,re
class ToolOutputNormalizer:
 pattern=re.compile(r'(?i)(api[_-]?key|access[_-]?token|password)(\\s*[:=]\\s*)([^\\s,;]+)')
 def __init__(self,max_chars=4000):
  if max_chars<32: raise ValueError("minimum limit is 32")
  self.max_chars=max_chars
 def normalize(self,name,value):
  if not name or len(name)>100: raise ValueError("invalid tool name")
  raw=json.dumps(value,sort_keys=True,ensure_ascii=False,default=lambda x:f"<unsupported:{type(x).__name__}>",allow_nan=False)
  raw=self.pattern.sub(lambda m:m.group(1)+m.group(2)+"[REDACTED]",raw)
  return {"tool":name,"trust":"untrusted","content":raw[:self.max_chars],"truncated":len(raw)>self.max_chars}

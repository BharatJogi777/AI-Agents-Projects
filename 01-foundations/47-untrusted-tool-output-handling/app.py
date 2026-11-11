"""AG-047: Normalize and bound tool output before it re-enters model context."""
import json,re
class ToolOutputNormalizer:
 # Redact string values of common credential fields in serialized JSON.
 pattern=re.compile(r'(?i)("(?:api[_-]?key|access[_-]?token|password)"\\s*:\\s*")[^"]*(")')
 def __init__(self,max_chars=4000):
  if max_chars<32: raise ValueError("minimum limit is 32")
  self.max_chars=max_chars
 def normalize(self,name,value):
  if not name or len(name)>100: raise ValueError("invalid tool name")
  raw=json.dumps(value,sort_keys=True,ensure_ascii=False,default=lambda x:f"<unsupported:{type(x).__name__}>",allow_nan=False)
  raw=self.pattern.sub(lambda m:m.group(1)+"[REDACTED]"+m.group(2),raw)
  return {"tool":name,"trust":"untrusted","content":raw[:self.max_chars],"truncated":len(raw)>self.max_chars}

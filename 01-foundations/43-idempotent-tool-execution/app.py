"""AG-043: Idempotent tool execution. Bind idempotency keys to canonical JSON fingerprints; replay matching results and reject key reuse with different inputs."""
import hashlib,json
from threading import RLock
class IdempotencyConflict(ValueError): pass
class IdempotentExecutor:
 def __init__(self): self.records={}; self.lock=RLock()
 def execute(self,key,payload,handler):
  if not isinstance(key,str) or not key or len(key)>128: raise ValueError("invalid idempotency key")
  raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
  digest=hashlib.sha256(raw.encode()).hexdigest()
  with self.lock:
   if key in self.records:
    old,result=self.records[key]
    if old!=digest: raise IdempotencyConflict("key reused with different payload")
    return result
   result=handler(dict(payload)); self.records[key]=(digest,result); return result

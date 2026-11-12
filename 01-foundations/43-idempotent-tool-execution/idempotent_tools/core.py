import hashlib,json
from dataclasses import dataclass
from threading import Condition,RLock
class IdempotencyConflict(ValueError):pass
class IdempotencyExecutionError(RuntimeError):pass
@dataclass(frozen=True)
class Record:fingerprint:str;result:object
def fingerprint(payload):
 try:raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
 except (TypeError,ValueError) as e:raise ValueError("payload must be finite JSON data") from e
 return hashlib.sha256(raw.encode()).hexdigest()
class IdempotentExecutor:
 """In-process deduplication; external side effects still require durable transactional idempotency."""
 def __init__(self,max_records=10000):
  if max_records<1:raise ValueError("max_records must be positive")
  self._max=max_records;self._records={};self._busy={};self._cv=Condition(RLock())
 def execute(self,key,payload,handler):
  if not isinstance(key,str) or not key.strip() or len(key)>128:raise ValueError("invalid idempotency key")
  if not callable(handler):raise TypeError("handler must be callable")
  digest=fingerprint(payload)
  with self._cv:
   while key in self._busy:
    if self._busy[key]!=digest:raise IdempotencyConflict("key reused with different payload")
    self._cv.wait()
   old=self._records.get(key)
   if old:
    if old.fingerprint!=digest:raise IdempotencyConflict("key reused with different payload")
    return old.result
   if len(self._records)>=self._max:raise RuntimeError("idempotency store full")
   self._busy[key]=digest
  try:result=handler(payload)
  except Exception as e:
   with self._cv:self._busy.pop(key,None);self._cv.notify_all()
   raise IdempotencyExecutionError("tool failed; retry is permitted") from e
  with self._cv:
   self._records[key]=Record(digest,result);self._busy.pop(key,None);self._cv.notify_all();return result
 def forget(self,key):
  with self._cv:
   if key in self._busy:raise RuntimeError("key is in flight")
   return self._records.pop(key,None) is not None

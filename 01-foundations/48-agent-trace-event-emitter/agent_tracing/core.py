from dataclasses import dataclass
from datetime import datetime,timezone
from threading import RLock
SENSITIVE={"password","token","api_key","authorization","secret","client_secret"}
@dataclass(frozen=True)
class TraceEvent:
 run_id:str;sequence:int;name:str;timestamp:datetime;attributes:dict
class TraceEmitter:
 def __init__(self,run_id,sink,max_attributes=20,max_value_chars=500,clock=lambda:datetime.now(timezone.utc)):
  if not isinstance(run_id,str) or not run_id or len(run_id)>128 or not callable(sink):raise ValueError("valid run_id and sink required")
  if max_attributes<0 or max_value_chars<1:raise ValueError("invalid bounds")
  self.run_id=run_id;self.sink=sink;self.max_attributes=max_attributes;self.max_value_chars=max_value_chars;self.clock=clock;self._seq=0;self._lock=RLock()
 def _sanitize(self,attrs):
  if not isinstance(attrs,dict):raise TypeError("attributes must be a dict")
  if len(attrs)>self.max_attributes:raise ValueError("too many attributes")
  out={}
  for key,value in attrs.items():
   if not isinstance(key,str) or not key or len(key)>100:raise ValueError("invalid attribute key")
   normalized=key.lower().replace("-","_")
   if normalized in SENSITIVE:out[key]="[REDACTED]"
   elif isinstance(value,str):out[key]=value[:self.max_value_chars]
   elif value is None or isinstance(value,(bool,int)):out[key]=value
   elif isinstance(value,float):out[key]=value if value==value and abs(value)!=float("inf") else "[NON_FINITE]"
   else:out[key]=f"[UNSUPPORTED:{type(value).__name__}]"
  return out
 def emit(self,name,attributes=None):
  if not isinstance(name,str) or not name or len(name)>100:raise ValueError("invalid event name")
  safe=self._sanitize(attributes or {})
  with self._lock:
   self._seq+=1
   event=TraceEvent(self.run_id,self._seq,name,self.clock(),safe)
   # Keep sink invocation serialized so observed order matches sequence.
   self.sink(event)
   return event

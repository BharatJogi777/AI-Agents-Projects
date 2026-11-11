"""AG-048: Agent trace event emitter. Emit ordered structured lifecycle events with bounded attributes, UTC timestamps, and common sensitive-field redaction."""
from dataclasses import dataclass
from datetime import datetime,timezone
from threading import Lock
SENSITIVE={"password","token","api_key","authorization","secret"}
@dataclass(frozen=True)
class TraceEvent: run_id:str; sequence:int; name:str; timestamp:str; attributes:dict
class TraceEmitter:
 def __init__(self,run_id,sink,max_attributes=20,max_value_chars=500):
  if not run_id or not callable(sink): raise ValueError("run_id and sink required")
  self.run_id=run_id; self.sink=sink; self.max_attributes=max_attributes; self.max_value_chars=max_value_chars; self.seq=0; self.lock=Lock()
 def emit(self,name,attributes=None):
  if not name or len(name)>100: raise ValueError("invalid event name")
  attrs=attributes or {}
  if len(attrs)>self.max_attributes: raise ValueError("too many attributes")
  safe={k:("[REDACTED]" if k.lower() in SENSITIVE else v[:self.max_value_chars] if isinstance(v,str) else v if isinstance(v,(int,float,bool)) or v is None else f"<{type(v).__name__}>") for k,v in attrs.items()}
  with self.lock:
   self.seq+=1; e=TraceEvent(self.run_id,self.seq,name,datetime.now(timezone.utc).isoformat(),safe); self.sink(e); return e

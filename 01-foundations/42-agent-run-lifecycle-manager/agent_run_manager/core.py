from dataclasses import dataclass
from datetime import datetime,timezone
from enum import Enum
from threading import RLock
from uuid import uuid4
class Status(str,Enum):
 CREATED="created";RUNNING="running";SUCCEEDED="succeeded";FAILED="failed";CANCELLED="cancelled"
TERMINAL=frozenset({Status.SUCCEEDED,Status.FAILED,Status.CANCELLED})
class InvalidLifecycle(ValueError):pass
class RunNotFound(KeyError):pass
@dataclass(frozen=True)
class Run:
 id:str;status:Status;created_at:datetime;started_at:datetime|None=None;finished_at:datetime|None=None;error:str|None=None
class RunManager:
 def __init__(self,max_runs=10000,clock=lambda:datetime.now(timezone.utc)):
  if max_runs<1:raise ValueError("max_runs must be positive")
  self._max=max_runs;self._clock=clock;self._runs={};self._lock=RLock()
 def create(self,run_id=None):
  with self._lock:
   key=run_id or str(uuid4())
   if not isinstance(key,str) or not key or len(key)>128:raise ValueError("invalid run id")
   if key in self._runs:raise ValueError("duplicate run id")
   if len(self._runs)>=self._max:raise RuntimeError("registry capacity reached")
   r=Run(key,Status.CREATED,self._clock());self._runs[key]=r;return r
 def get(self,key):
  with self._lock:
   if key not in self._runs:raise RunNotFound(key)
   return self._runs[key]
 def list_runs(self,status=None):
  with self._lock:return tuple(r for r in self._runs.values() if status is None or r.status is status)
 def start(self,key):
  with self._lock:
   r=self.get(key)
   if r.status is not Status.CREATED:raise InvalidLifecycle("only created runs can start")
   u=Run(r.id,Status.RUNNING,r.created_at,self._clock());self._runs[key]=u;return u
 def finish(self,key,status,error=None):
  if status not in TERMINAL:raise InvalidLifecycle("terminal status required")
  if error is not None and (not isinstance(error,str) or len(error)>1000):raise ValueError("error must be <=1000 chars")
  with self._lock:
   r=self.get(key)
   if r.status is not Status.RUNNING:raise InvalidLifecycle("only running runs can finish")
   u=Run(r.id,status,r.created_at,r.started_at,self._clock(),error);self._runs[key]=u;return u
 def delete(self,key):
  with self._lock:
   r=self.get(key)
   if r.status not in TERMINAL:raise InvalidLifecycle("active run cannot be deleted")
   del self._runs[key]

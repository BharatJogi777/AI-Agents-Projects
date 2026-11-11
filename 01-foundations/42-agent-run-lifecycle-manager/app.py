"""AG-042: Agent run lifecycle manager. Thread-safe in-memory run registry with isolated IDs, UTC lifecycle timestamps, and validated completion."""
from dataclasses import dataclass
from datetime import datetime,timezone
from enum import Enum
from threading import RLock
from uuid import uuid4
class Status(str,Enum): CREATED="created"; RUNNING="running"; SUCCEEDED="succeeded"; FAILED="failed"; CANCELLED="cancelled"
class InvalidLifecycle(ValueError): pass
@dataclass
class Run:
 id:str; status:Status; created_at:datetime; started_at:datetime|None=None; finished_at:datetime|None=None; error:str|None=None
class RunManager:
 def __init__(self): self.runs={}; self.lock=RLock()
 def create(self):
  with self.lock:
   r=Run(str(uuid4()),Status.CREATED,datetime.now(timezone.utc)); self.runs[r.id]=r; return r
 def get(self,i):
  with self.lock:
   if i not in self.runs: raise KeyError(i)
   return self.runs[i]
 def start(self,i):
  with self.lock:
   r=self.get(i)
   if r.status is not Status.CREATED: raise InvalidLifecycle("not created")
   r.status=Status.RUNNING; r.started_at=datetime.now(timezone.utc); return r
 def finish(self,i,status,error=None):
  if status not in {Status.SUCCEEDED,Status.FAILED,Status.CANCELLED}: raise InvalidLifecycle("terminal status required")
  with self.lock:
   r=self.get(i)
   if r.status is not Status.RUNNING: raise InvalidLifecycle("not running")
   r.status=status; r.finished_at=datetime.now(timezone.utc); r.error=error[:500] if error else None; return r

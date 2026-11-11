from dataclasses import dataclass
from enum import Enum
class Status(str,Enum):PENDING="pending";RUNNING="running";SUCCEEDED="succeeded";FAILED="failed";SKIPPED="skipped"
@dataclass
class StepState:id:str;depends_on:tuple[str,...]=();status:Status=Status.PENDING;error:str|None=None
class ExecutionTracker:
 def __init__(self,steps):
  self.steps={s.id:s for s in steps}
  if len(self.steps)!=len(steps):raise ValueError("duplicate IDs")
  for s in steps:
   if any(d not in self.steps or d==s.id for d in s.depends_on):raise ValueError("invalid dependency")
 def ready(self,k):
  s=self.steps[k];return s.status==Status.PENDING and all(self.steps[d].status==Status.SUCCEEDED for d in s.depends_on)
 def transition(self,k,target,error=None):
  s=self.steps[k]
  if s.status==target and target in (Status.SUCCEEDED,Status.FAILED,Status.SKIPPED):return s
  allowed={Status.PENDING:{Status.RUNNING,Status.SKIPPED},Status.RUNNING:{Status.SUCCEEDED,Status.FAILED},Status.FAILED:{Status.PENDING}}
  if target not in allowed.get(s.status,set()):raise ValueError("invalid transition")
  if target==Status.RUNNING and not self.ready(k):raise ValueError("dependencies incomplete")
  s.status=target;s.error=error if target==Status.FAILED else None;return s
 def snapshot(self):return {k:v.status.value for k,v in self.steps.items()}

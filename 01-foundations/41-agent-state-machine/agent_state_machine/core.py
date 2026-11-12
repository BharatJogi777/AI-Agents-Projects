from dataclasses import dataclass
from datetime import datetime,timezone
from enum import Enum
from threading import RLock
class State(str,Enum):
 CREATED="created"; RUNNING="running"; WAITING="waiting"; SUCCEEDED="succeeded"; FAILED="failed"; CANCELLED="cancelled"
TERMINAL=frozenset({State.SUCCEEDED,State.FAILED,State.CANCELLED})
ALLOWED={State.CREATED:{State.RUNNING,State.CANCELLED},State.RUNNING:{State.WAITING,State.SUCCEEDED,State.FAILED,State.CANCELLED},State.WAITING:{State.RUNNING,State.FAILED,State.CANCELLED}}
class InvalidTransition(ValueError): pass
@dataclass(frozen=True)
class Transition:
 sequence:int; previous:State|None; current:State; occurred_at:datetime; reason:str|None=None
class AgentStateMachine:
 def __init__(self,clock=lambda:datetime.now(timezone.utc)):
  self._state=State.CREATED; self._clock=clock; self._lock=RLock(); self._history=[Transition(1,None,State.CREATED,clock(),"initialized")]
 @property
 def state(self):
  with self._lock:return self._state
 @property
 def terminal(self):return self.state in TERMINAL
 def history(self):
  with self._lock:return tuple(self._history)
 def transition(self,target,reason=None):
  if not isinstance(target,State):raise TypeError("target must be State")
  if reason is not None and (not isinstance(reason,str) or len(reason)>500):raise ValueError("reason must be <=500 chars")
  with self._lock:
   if target not in ALLOWED.get(self._state,set()):raise InvalidTransition(f"{self._state.value} -> {target.value} is invalid")
   old=self._state;self._state=target;e=Transition(len(self._history)+1,old,target,self._clock(),reason);self._history.append(e);return e

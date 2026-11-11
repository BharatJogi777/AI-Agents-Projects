"""AG-041: Agent state machine. Finite-state machine for legal agent-run transitions, immutable terminal states, and transition history."""
from dataclasses import dataclass,field
from enum import Enum
class State(str,Enum): CREATED="created"; RUNNING="running"; WAITING="waiting"; SUCCEEDED="succeeded"; FAILED="failed"; CANCELLED="cancelled"
TERMINAL={State.SUCCEEDED,State.FAILED,State.CANCELLED}
ALLOWED={State.CREATED:{State.RUNNING,State.CANCELLED},State.RUNNING:{State.WAITING,State.SUCCEEDED,State.FAILED,State.CANCELLED},State.WAITING:{State.RUNNING,State.FAILED,State.CANCELLED}}
class InvalidTransition(ValueError): pass
@dataclass
class AgentStateMachine:
 state:State=State.CREATED
 history:list[State]=field(default_factory=lambda:[State.CREATED])
 def transition(self,target):
  if target not in ALLOWED.get(self.state,set()): raise InvalidTransition(f"{self.state.value} -> {target.value}")
  self.state=target; self.history.append(target); return target
 @property
 def terminal(self): return self.state in TERMINAL

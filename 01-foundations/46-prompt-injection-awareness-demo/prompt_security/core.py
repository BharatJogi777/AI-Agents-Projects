from dataclasses import dataclass
from enum import Enum
class Trust(str,Enum):TRUSTED="trusted";UNTRUSTED="untrusted"
@dataclass(frozen=True)
class PromptParts:policy:str;request:str;retrieved:str
@dataclass(frozen=True)
class ActionDecision:allowed:bool;requires_approval:bool;reason:str
class PromptBuilder:
 def __init__(self,max_chars=12000):
  if max_chars<100:raise ValueError("max_chars must be >=100")
  self.max_chars=max_chars
 def build(self,parts):
  values=(parts.policy,parts.request,parts.retrieved)
  if any(not isinstance(x,str) for x in values):raise TypeError("prompt sections must be strings")
  if sum(map(len,values))>self.max_chars:raise ValueError("prompt exceeds configured character budget")
  return ("TRUSTED POLICY:\n"+parts.policy+"\n\nUSER REQUEST (untrusted):\n<user_input>\n"+parts.request+
   "\n</user_input>\n\nRETRIEVED DATA (untrusted):\n<retrieved_data>\n"+parts.retrieved+"\n</retrieved_data>")
 @staticmethod
 def allowed(action,allowlist,approved=False):return action in allowlist and approved
class ActionPolicy:
 def __init__(self,allowed_actions,approval_required=()):
  self._allowed=frozenset(allowed_actions);self._approval=frozenset(approval_required)
  if any(not isinstance(a,str) or not a for a in self._allowed|self._approval):raise ValueError("action names must be non-empty strings")
 def evaluate(self,action,approved=False):
  if action not in self._allowed:return ActionDecision(False,False,"action_not_allowlisted")
  if action in self._approval and not approved:return ActionDecision(False,True,"human_approval_required")
  return ActionDecision(True,False,"allowed")

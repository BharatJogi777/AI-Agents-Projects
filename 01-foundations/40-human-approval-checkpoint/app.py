from dataclasses import dataclass
from hashlib import sha256
import json,secrets
@dataclass(frozen=True)
class Approval:id:str;action_hash:str;status:str;expires_at:float;reason:str|None=None
class ApprovalGate:
 def __init__(self,clock):self.clock=clock;self._items={}
 @staticmethod
 def _hash(action):return sha256(json.dumps(action,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
 def request(self,action,ttl_seconds=300):
  if not isinstance(action,dict) or not action or ttl_seconds<=0:raise ValueError("invalid action or TTL")
  a=Approval(secrets.token_urlsafe(18),self._hash(action),"pending",self.clock()+ttl_seconds);self._items[a.id]=a;return a
 def decide(self,approval_id,action,approved,reason=None):
  a=self._items[approval_id]
  if a.status!="pending":raise ValueError("already decided")
  if self.clock()>=a.expires_at:
   self._items[a.id]=Approval(a.id,a.action_hash,"expired",a.expires_at);raise TimeoutError("approval expired")
  if self._hash(action)!=a.action_hash:raise PermissionError("action payload changed")
  a=Approval(a.id,a.action_hash,"approved" if approved else "rejected",a.expires_at,reason);self._items[a.id]=a;return a
 def get(self,approval_id):return self._items[approval_id]

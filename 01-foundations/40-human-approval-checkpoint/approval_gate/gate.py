from dataclasses import replace
from hashlib import sha256
from threading import RLock
import json,math,secrets
from .contracts import Approval,ApprovalNotFound
def canonical_action_hash(action)->str:
    try:encoded=json.dumps(action,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
    except (TypeError,ValueError) as exc:raise ValueError("action must be canonical JSON data") from exc
    return sha256(encoded).hexdigest()
class ApprovalGate:
    """Process-local one-time approval gate. Durable deployments need transactional persistence."""
    def __init__(self,clock):
        if not callable(clock):raise TypeError("clock must be callable")
        self.clock=clock;self._items={};self._lock=RLock()
    def request(self,action,ttl_seconds=300):
        if not isinstance(action,dict) or not action:raise ValueError("action must be a non-empty object")
        if isinstance(ttl_seconds,bool) or not isinstance(ttl_seconds,(int,float)) or not math.isfinite(ttl_seconds) or ttl_seconds<=0:raise ValueError("TTL must be finite and positive")
        now=self.clock()
        if isinstance(now,bool) or not isinstance(now,(int,float)) or not math.isfinite(now):raise ValueError("clock must return a finite number")
        item=Approval(secrets.token_urlsafe(24),canonical_action_hash(action),"pending",now+ttl_seconds)
        with self._lock:self._items[item.id]=item
        return item
    def decide(self,approval_id,action,approved,reason=None):
        if type(approved) is not bool:raise ValueError("approved must be boolean")
        if reason is not None and (not isinstance(reason,str) or len(reason)>1000):raise ValueError("reason must be text up to 1000 chars")
        digest=canonical_action_hash(action)
        with self._lock:
            item=self._items.get(approval_id)
            if item is None:raise ApprovalNotFound(approval_id)
            if item.status!="pending":raise ValueError("approval already decided or expired")
            now=self.clock()
            if now>=item.expires_at:
                self._items[item.id]=replace(item,status="expired")
                raise TimeoutError("approval expired")
            if not secrets.compare_digest(digest,item.action_hash):raise PermissionError("action payload changed")
            updated=replace(item,status="approved" if approved else "rejected",reason=reason)
            self._items[item.id]=updated
            return updated
    def get(self,approval_id):
        with self._lock:
            item=self._items.get(approval_id)
            if item is None:raise ApprovalNotFound(approval_id)
            if item.status=="pending" and self.clock()>=item.expires_at:
                item=replace(item,status="expired");self._items[item.id]=item
            return item

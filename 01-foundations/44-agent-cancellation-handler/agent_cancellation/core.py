from dataclasses import dataclass
from threading import Event,Lock
from time import monotonic
class AgentCancelled(RuntimeError):
 def __init__(self,reason):self.reason=reason;super().__init__(reason)
@dataclass(frozen=True)
class Cancellation:reason:str;requested_at:float
class CancellationToken:
 def __init__(self,clock=monotonic):
  self._event=Event();self._lock=Lock();self._clock=clock;self._request=None
 def cancel(self,reason="cancelled"):
  if not isinstance(reason,str):raise TypeError("reason must be text")
  reason=reason.strip()[:200] or "cancelled"
  with self._lock:
   if self._request is not None:return False
   self._request=Cancellation(reason,self._clock());self._event.set();return True
 @property
 def cancelled(self):return self._event.is_set()
 @property
 def reason(self):
  with self._lock:return self._request.reason if self._request else None
 @property
 def requested_at(self):
  with self._lock:return self._request.requested_at if self._request else None
 def wait(self,timeout=None):return self._event.wait(timeout)
 def checkpoint(self):
  with self._lock:r=self._request
  if r is not None:raise AgentCancelled(r.reason)
def run_steps(steps,token):
 results=[]
 for step in steps:
  token.checkpoint();results.append(step())
 token.checkpoint();return results

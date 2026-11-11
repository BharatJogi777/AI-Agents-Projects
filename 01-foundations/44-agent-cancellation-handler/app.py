"""AG-044: Agent cancellation handler. Thread-safe cooperative cancellation token with first-reason-wins semantics and checkpoints between agent steps."""
from threading import Event,Lock
class AgentCancelled(Exception): pass
class CancellationToken:
 def __init__(self): self.event=Event(); self.lock=Lock(); self._reason="cancelled"
 def cancel(self,reason="cancelled"):
  with self.lock:
   if self.event.is_set(): return False
   self._reason=(reason or "cancelled")[:200]; self.event.set(); return True
 @property
 def cancelled(self): return self.event.is_set()
 @property
 def reason(self): return self._reason if self.cancelled else None
 def checkpoint(self):
  if self.cancelled: raise AgentCancelled(self._reason)

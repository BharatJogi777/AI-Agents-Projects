from threading import RLock
from .contracts import Status,StepState
class ExecutionTracker:
    """In-memory state machine; callers persist snapshots/events for crash recovery."""
    _allowed={Status.PENDING:{Status.RUNNING,Status.SKIPPED},Status.RUNNING:{Status.SUCCEEDED,Status.FAILED},Status.FAILED:{Status.PENDING}}
    def __init__(self,steps):
        if not isinstance(steps,(list,tuple)) or not steps:raise ValueError("steps required")
        if any(not isinstance(s,StepState) or not isinstance(s.id,str) or not s.id for s in steps):raise ValueError("invalid step")
        self.steps={s.id:s for s in steps}
        if len(self.steps)!=len(steps):raise ValueError("invalid or duplicate IDs")
        for s in steps:
            if not isinstance(s.depends_on,tuple) or any(not isinstance(d,str) or d not in self.steps or d==s.id for d in s.depends_on) or len(set(s.depends_on))!=len(s.depends_on):raise ValueError("invalid dependency")
        visiting=set();visited=set()
        def visit(key):
            if key in visiting:raise ValueError("dependency cycle")
            if key in visited:return
            visiting.add(key)
            for dep in self.steps[key].depends_on:visit(dep)
            visiting.remove(key);visited.add(key)
        for key in self.steps:visit(key)
        self._lock=RLock()
    def ready(self,key):
        with self._lock:
            if key not in self.steps:raise KeyError(key)
            s=self.steps[key]
            return s.status==Status.PENDING and all(self.steps[d].status==Status.SUCCEEDED for d in s.depends_on)
    def transition(self,key,target,error=None):
        with self._lock:
            if key not in self.steps:raise KeyError(key)
            s=self.steps[key]
            if not isinstance(target,Status):raise TypeError("target must be Status")
            if s.status==target and target in (Status.SUCCEEDED,Status.FAILED,Status.SKIPPED):return s
            if target not in self._allowed.get(s.status,set()):raise ValueError("invalid transition")
            if target==Status.RUNNING and not all(self.steps[d].status==Status.SUCCEEDED for d in s.depends_on):raise ValueError("dependencies incomplete")
            if target==Status.FAILED and (not isinstance(error,str) or not error.strip()):raise ValueError("failure requires a non-empty error")
            s.status=target;s.error=error if target==Status.FAILED else None
            return s
    def snapshot(self):
        with self._lock:return {k:{"status":v.status.value,"depends_on":list(v.depends_on),"error":v.error} for k,v in self.steps.items()}

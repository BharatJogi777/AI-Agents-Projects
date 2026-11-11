from datetime import datetime,timezone
from threading import RLock
from .contracts import Preference
ALLOWED_CATEGORIES=frozenset({"format","language","response_style","technical_stack","learning_style"})
class PreferenceMemory:
    """Consent-gated in-memory preference store; no inferred or sensitive preferences."""
    def __init__(self,clock=None):
        self._items={};self._clock=clock or (lambda:datetime.now(timezone.utc));self._lock=RLock()
    def remember(self,user_id,category,value,confirmed_by_user):
        if not isinstance(user_id,str) or not user_id.strip():raise ValueError("user_id required")
        if category not in ALLOWED_CATEGORIES or not confirmed_by_user:raise PermissionError("only confirmed non-sensitive preferences may be stored")
        if not isinstance(value,str) or not value.strip() or len(value)>200:raise ValueError("invalid value")
        recorded=self._clock()
        if not isinstance(recorded,datetime) or recorded.tzinfo is None:raise ValueError("clock must return timezone-aware datetime")
        pref=Preference(category,value.strip(),True,recorded.astimezone(timezone.utc).isoformat())
        with self._lock:self._items[(user_id,category)]=pref
        return pref
    def get(self,user_id):
        with self._lock:return tuple(v for (u,_),v in self._items.items() if u==user_id)
    def forget(self,user_id,category=None):
        if category is not None and category not in ALLOWED_CATEGORIES:raise ValueError("unknown preference category")
        with self._lock:
            keys=[k for k in self._items if k[0]==user_id and (category is None or k[1]==category)]
            for key in keys:del self._items[key]
            return len(keys)

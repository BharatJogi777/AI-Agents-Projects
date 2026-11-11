from threading import RLock
from time import monotonic
from collections import OrderedDict
import math
from .contracts import Entry
class SessionMemoryStore:
    """Thread-safe bounded TTL store. Capacity is global across all sessions."""
    def __init__(self,max_entries:int=1000,clock=monotonic,max_value_chars:int=20000):
        if type(max_entries) is not int or max_entries<1:raise ValueError("capacity must be positive")
        if type(max_value_chars) is not int or max_value_chars<1:raise ValueError("value limit must be positive")
        self.max_entries=max_entries;self.clock=clock;self.max_value_chars=max_value_chars;self._data=OrderedDict();self._lock=RLock()
    def _purge(self,now):
        for key in [key for key,entry in self._data.items() if entry.expires_at<=now]:self._data.pop(key,None)
    def put(self,session_id,key,value,ttl_seconds):
        if not isinstance(session_id,str) or not session_id.strip() or not isinstance(key,str) or not key.strip() or not isinstance(value,str) or len(value)>self.max_value_chars:raise ValueError("invalid entry")
        if isinstance(ttl_seconds,bool) or not isinstance(ttl_seconds,(int,float)) or not math.isfinite(ttl_seconds) or ttl_seconds<=0:raise ValueError("TTL must be finite and positive")
        with self._lock:
            now=self.clock();self._purge(now);item=(session_id,key)
            if item not in self._data and len(self._data)>=self.max_entries:raise OverflowError("capacity reached")
            self._data[item]=Entry(value,now+ttl_seconds,now);self._data.move_to_end(item)
    def get(self,session_id,key):
        with self._lock:
            now=self.clock();item=(session_id,key);entry=self._data.get(item)
            if entry is None:return None
            if entry.expires_at<=now:self._data.pop(item,None);return None
            self._data.move_to_end(item);return entry.value
    def delete_session(self,session_id):
        with self._lock:
            keys=[key for key in self._data if key[0]==session_id]
            for key in keys:del self._data[key]
            return len(keys)
    def size(self):
        with self._lock:self._purge(self.clock());return len(self._data)

from dataclasses import dataclass
from threading import RLock
from time import monotonic
@dataclass
class Entry:value:str;expires_at:float
class SessionMemoryStore:
 def __init__(self,max_entries=1000,clock=monotonic):
  if max_entries<1:raise ValueError("capacity must be positive")
  self.max_entries=max_entries;self.clock=clock;self._data={};self._lock=RLock()
 def _purge(self):
  now=self.clock()
  for k in [k for k,v in self._data.items() if v.expires_at<=now]:del self._data[k]
 def put(self,session_id,key,value,ttl_seconds):
  if not session_id or not key or not isinstance(value,str) or ttl_seconds<=0:raise ValueError("invalid entry")
  with self._lock:
   self._purge();k=(session_id,key)
   if k not in self._data and len(self._data)>=self.max_entries:raise OverflowError("capacity reached")
   self._data[k]=Entry(value,self.clock()+ttl_seconds)
 def get(self,session_id,key):
  with self._lock:
   x=self._data.get((session_id,key))
   if x is None:return None
   if x.expires_at<=self.clock():self._data.pop((session_id,key),None);return None
   return x.value
 def delete_session(self,session_id):
  with self._lock:
   keys=[k for k in self._data if k[0]==session_id]
   for k in keys:del self._data[k]
   return len(keys)

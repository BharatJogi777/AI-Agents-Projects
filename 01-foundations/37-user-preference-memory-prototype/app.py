from dataclasses import dataclass
from datetime import datetime,timezone
ALLOWED={"format","language","response_style","technical_stack","learning_style"}
@dataclass(frozen=True)
class Preference:category:str;value:str;confirmed_by_user:bool;recorded_at:str
class PreferenceMemory:
 def __init__(self):self._items={}
 def remember(self,user_id,category,value,confirmed_by_user):
  if not user_id or category not in ALLOWED or not confirmed_by_user:raise PermissionError("only confirmed non-sensitive preferences may be stored")
  if not value.strip() or len(value)>200:raise ValueError("invalid value")
  p=Preference(category,value,True,datetime.now(timezone.utc).isoformat());self._items[(user_id,category)]=p;return p
 def get(self,user_id):return tuple(v for (u,_),v in self._items.items() if u==user_id)
 def forget(self,user_id,category=None):
  keys=[k for k in self._items if k[0]==user_id and (category is None or k[1]==category)]
  for k in keys:del self._items[k]
  return len(keys)

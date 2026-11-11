from dataclasses import dataclass
@dataclass(frozen=True)
class Message:role:str;content:str;turn_id:str|None=None
class ShortTermMemory:
 def __init__(self,max_messages=20):
  if max_messages<2:raise ValueError("max_messages must be >=2")
  self.max_messages=max_messages;self._messages=[]
 def append(self,m):
  if m.role not in ("system","user","assistant") or not m.content.strip():raise ValueError("invalid message")
  if (m.role=="system" and m.turn_id is not None) or (m.role!="system" and not m.turn_id):raise ValueError("invalid turn ID")
  self._messages.append(m);self._trim()
 def _trim(self):
  while len(self._messages)>self.max_messages:
   sys=[m for m in self._messages if m.role=="system"];rest=[m for m in self._messages if m.role!="system"]
   if len(rest)<2:raise ValueError("cannot preserve mandatory messages")
   old=rest[0].turn_id;self._messages=sys+[m for m in rest if m.turn_id!=old]
 def snapshot(self):return tuple(self._messages)
 def clear(self):self._messages.clear()

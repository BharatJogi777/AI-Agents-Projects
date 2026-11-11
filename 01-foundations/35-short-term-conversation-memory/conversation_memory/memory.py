from threading import RLock
from .contracts import Message
class ShortTermMemory:
    """Bounded chronological memory; system messages are retained and turns evicted atomically."""
    def __init__(self,max_messages:int=20,max_message_chars:int=20000):
        if type(max_messages) is not int or max_messages<2:raise ValueError("max_messages must be >= 2")
        if type(max_message_chars) is not int or max_message_chars<1:raise ValueError("max_message_chars must be positive")
        self.max_messages=max_messages;self.max_message_chars=max_message_chars;self._messages=[];self._lock=RLock()
    def append(self,message:Message):
        if not isinstance(message,Message) or message.role not in ("system","user","assistant") or not isinstance(message.content,str) or not message.content.strip() or len(message.content)>self.max_message_chars:raise ValueError("invalid message")
        if (message.role=="system" and message.turn_id is not None) or (message.role!="system" and (not isinstance(message.turn_id,str) or not message.turn_id)):raise ValueError("invalid turn ID")
        with self._lock:
            candidate=self._messages+[message]
            systems=[m for m in candidate if m.role=="system"]
            if len(systems)>=self.max_messages and len(candidate)>self.max_messages:raise ValueError("system messages exceed memory capacity")
            while len(candidate)>self.max_messages:
                non_system=[m for m in candidate if m.role!="system"]
                if not non_system:raise ValueError("cannot evict mandatory system messages")
                oldest=non_system[0].turn_id
                candidate=systems+[m for m in non_system if m.turn_id!=oldest]
            self._messages=candidate
    def snapshot(self):
        with self._lock:return tuple(self._messages)
    def clear(self):
        with self._lock:self._messages.clear()

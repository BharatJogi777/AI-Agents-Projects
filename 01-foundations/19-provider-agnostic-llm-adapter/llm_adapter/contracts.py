from dataclasses import dataclass,field
from types import MappingProxyType
from typing import Any,Mapping

_ALLOWED_ROLES={"system","user","assistant","tool"}

@dataclass(frozen=True)
class ChatMessage:
    role:str
    content:str
    def __post_init__(self):
        if self.role not in _ALLOWED_ROLES: raise ValueError("unsupported message role")
        if not isinstance(self.content,str): raise TypeError("message content must be text")
        if len(self.content.encode("utf-8"))>1_000_000: raise ValueError("message content exceeds 1 MB")

@dataclass(frozen=True)
class ChatRequest:
    messages:tuple[ChatMessage,...]
    model:str
    temperature:float=0.0
    max_tokens:int=512
    metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if not self.messages or any(not isinstance(m,ChatMessage) for m in self.messages): raise ValueError("messages must be a non-empty tuple of ChatMessage")
        if not isinstance(self.model,str) or not self.model.strip() or len(self.model)>200: raise ValueError("model is required and must be <= 200 characters")
        if not 0<=self.temperature<=2: raise ValueError("temperature must be 0..2")
        if type(self.max_tokens) is not int or not 1<=self.max_tokens<=32768: raise ValueError("max_tokens must be 1..32768")
        object.__setattr__(self,"messages",tuple(self.messages))
        object.__setattr__(self,"metadata",MappingProxyType(dict(self.metadata)))

@dataclass(frozen=True)
class ChatResponse:
    content:str
    model:str
    finish_reason:str|None=None
    usage:Mapping[str,int]=field(default_factory=dict)
    raw:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if not isinstance(self.content,str) or not isinstance(self.model,str) or not self.model.strip(): raise ValueError("response content and model must be strings")
        if self.finish_reason is not None and not isinstance(self.finish_reason,str): raise TypeError("finish_reason must be text or None")
        usage=dict(self.usage)
        if any(not isinstance(k,str) or type(v) is not int or v<0 for k,v in usage.items()): raise ValueError("usage values must be non-negative integers")
        object.__setattr__(self,"usage",MappingProxyType(usage))
        object.__setattr__(self,"raw",MappingProxyType(dict(self.raw)))

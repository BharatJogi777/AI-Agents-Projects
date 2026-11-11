"""Minimal provider-neutral request/response contracts used by AG-020."""
from dataclasses import dataclass,field
from typing import Any


@dataclass(frozen=True)
class ChatMessage:
    role:str
    content:str
    def __post_init__(self):
        if self.role not in {"system","user","assistant"}: raise ValueError("unsupported Ollama text role")
        if not isinstance(self.content,str): raise TypeError("content must be text")


@dataclass(frozen=True)
class ChatRequest:
    messages:tuple[ChatMessage,...]
    model:str
    temperature:float=0.0
    max_tokens:int=512
    def __post_init__(self):
        if not self.messages: raise ValueError("messages cannot be empty")
        if not self.model.strip(): raise ValueError("model is required")
        if not 0<=self.temperature<=2: raise ValueError("temperature must be 0..2")
        if not 1<=self.max_tokens<=32768: raise ValueError("max_tokens must be 1..32768")


@dataclass(frozen=True)
class ChatResponse:
    content:str
    model:str
    finish_reason:str|None=None
    usage:dict[str,int]=field(default_factory=dict)
    raw:dict[str,Any]=field(default_factory=dict)

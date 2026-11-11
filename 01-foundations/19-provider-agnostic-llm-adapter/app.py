"""Provider-neutral chat contracts and a small adapter facade."""
from dataclasses import dataclass,field
from typing import Any,Protocol


@dataclass(frozen=True)
class ChatMessage:
    role:str
    content:str
    def __post_init__(self):
        if self.role not in {"system","user","assistant","tool"}: raise ValueError("unsupported message role")
        if not isinstance(self.content,str): raise TypeError("message content must be text")


@dataclass(frozen=True)
class ChatRequest:
    messages:tuple[ChatMessage,...]
    model:str
    temperature:float=0.0
    max_tokens:int=512
    metadata:dict[str,Any]=field(default_factory=dict)
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


class LLMProvider(Protocol):
    def chat(self,request:ChatRequest)->ChatResponse: ...


class LLMClient:
    def __init__(self,providers:dict[str,LLMProvider],default_provider:str):
        if default_provider not in providers: raise ValueError("default provider is not registered")
        self.providers=dict(providers); self.default_provider=default_provider

    def chat(self,request:ChatRequest,provider:str|None=None)->ChatResponse:
        selected=provider or self.default_provider
        client=self.providers.get(selected)
        if client is None: raise ValueError(f"provider is not registered: {selected}")
        response=client.chat(request)
        if not isinstance(response,ChatResponse): raise TypeError("provider must return ChatResponse")
        return response

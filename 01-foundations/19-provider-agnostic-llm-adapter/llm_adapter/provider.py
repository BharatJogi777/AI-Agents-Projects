from typing import Protocol
from .contracts import ChatRequest,ChatResponse

class LLMProvider(Protocol):
    def chat(self,request:ChatRequest)->ChatResponse: ...
class ProviderNotRegistered(ValueError): pass
class ProviderContractError(TypeError): pass

class LLMClient:
    """Select a configured provider; never silently switch provider semantics."""
    def __init__(self,providers:dict[str,LLMProvider],default_provider:str):
        if not providers or default_provider not in providers: raise ValueError("default provider must be registered")
        if any(not isinstance(k,str) or not k.strip() for k in providers): raise ValueError("provider names must be non-empty strings")
        self.providers=dict(providers); self.default_provider=default_provider
    def chat(self,request:ChatRequest,provider:str|None=None)->ChatResponse:
        selected=provider or self.default_provider
        client=self.providers.get(selected)
        if client is None: raise ProviderNotRegistered(f"provider is not registered: {selected}")
        response=client.chat(request)
        if not isinstance(response,ChatResponse): raise ProviderContractError("provider must return ChatResponse")
        return response

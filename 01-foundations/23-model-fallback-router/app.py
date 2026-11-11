"""Sequential fallback routing using declared model capabilities."""
from dataclasses import dataclass
from typing import Protocol,Callable
from registry import CapabilityRegistry

class ChatProvider(Protocol):
    def chat(self,model_id:str,prompt:str)->str: ...

@dataclass(frozen=True)
class RouteResult:
    model_id:str
    response:str
    attempts:tuple[str,...]

class NoModelAvailable(RuntimeError): pass

class ModelFallbackRouter:
    def __init__(self,registry:CapabilityRegistry,providers:dict[str,ChatProvider],is_healthy:Callable[[str],bool]|None=None):
        self.registry=registry; self.providers=providers; self.is_healthy=is_healthy or (lambda _:True)
    def generate(self,prompt:str,*,provider_order:tuple[str,...]=(),tools=False,json_schema=False,min_context=1)->RouteResult:
        if not prompt.strip(): raise ValueError("prompt cannot be empty")
        rank={p:i for i,p in enumerate(provider_order)}
        models=self.registry.select(tools=tools,json_schema=json_schema,min_context=min_context)
        models.sort(key=lambda m:(min((rank.get(p,len(rank)) for p in m.providers),default=len(rank)),-m.context_tokens,m.model_id))
        attempts=[]
        for model in models:
            for name in model.providers:
                if provider_order and name not in rank: continue
                client=self.providers.get(name)
                if client is None or not self.is_healthy(name): continue
                attempts.append(f"{name}:{model.model_id}")
                try:
                    answer=client.chat(model.model_id,prompt)
                    if isinstance(answer,str) and answer.strip(): return RouteResult(model.model_id,answer,tuple(attempts))
                except Exception:
                    continue
        raise NoModelAvailable(f"no compatible model succeeded; attempted {len(attempts)} route(s)")

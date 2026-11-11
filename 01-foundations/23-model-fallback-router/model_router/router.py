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
    """Try only capability-compatible, healthy provider/model pairs in stable order."""
    def __init__(self,registry:CapabilityRegistry,providers:dict[str,ChatProvider],is_healthy:Callable[[str],bool]|None=None):
        self.registry=registry; self.providers=dict(providers); self.is_healthy=is_healthy or (lambda _:True)
    def generate(self,prompt:str,*,provider_order:tuple[str,...]=(),tools:bool=False,json_schema:bool=False,min_context:int=1)->RouteResult:
        if not isinstance(prompt,str) or not prompt.strip(): raise ValueError("prompt cannot be empty")
        rank={name:index for index,name in enumerate(provider_order)}
        models=self.registry.select(tools=tools,json_schema=json_schema,min_context=min_context)
        models.sort(key=lambda model:(min((rank.get(p,len(rank)) for p in model.providers),default=len(rank)),-model.context_tokens,model.model_id))
        attempts=[]
        for model in models:
            providers=sorted(model.providers,key=lambda p:(rank.get(p,len(rank)),p))
            for name in providers:
                if provider_order and name not in rank: continue
                client=self.providers.get(name)
                if client is None: continue
                try:
                    if not self.is_healthy(name): continue
                except Exception:
                    continue
                attempts.append(f"{name}:{model.model_id}")
                try:
                    answer=client.chat(model.model_id,prompt)
                    if isinstance(answer,str) and answer.strip(): return RouteResult(model.model_id,answer,tuple(attempts))
                except Exception:
                    # Provider internals are intentionally not copied into the result.
                    continue
        raise NoModelAvailable(f"no compatible model succeeded; attempted {len(attempts)} route(s)")

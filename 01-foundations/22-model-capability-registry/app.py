"""Explicit capability metadata and deterministic model selection."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelCapabilities:
    model_id:str
    providers:tuple[str,...]
    context_tokens:int
    max_output_tokens:int
    supports_tools:bool=False
    supports_json_schema:bool=False
    supports_vision:bool=False
    supports_streaming:bool=False
    def __post_init__(self):
        if not self.model_id.strip() or not self.providers: raise ValueError("model_id and providers required")
        if self.context_tokens<1 or not 1<=self.max_output_tokens<=self.context_tokens: raise ValueError("invalid token limits")

class CapabilityRegistry:
    def __init__(self): self._models={}
    def register(self,item:ModelCapabilities):
        if item.model_id in self._models: raise ValueError(f"duplicate model: {item.model_id}")
        self._models[item.model_id]=item
    def get(self,model_id):
        try: return self._models[model_id]
        except KeyError as exc: raise KeyError(f"unknown model: {model_id}") from exc
    def select(self,*,provider=None,tools=False,json_schema=False,vision=False,streaming=False,min_context=1):
        result=[]
        for m in self._models.values():
            if provider and provider not in m.providers: continue
            if tools and not m.supports_tools: continue
            if json_schema and not m.supports_json_schema: continue
            if vision and not m.supports_vision: continue
            if streaming and not m.supports_streaming: continue
            if m.context_tokens<min_context: continue
            result.append(m)
        return sorted(result,key=lambda x:(-x.context_tokens,x.model_id))

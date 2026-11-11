"""Small local capability registry for this standalone routing project."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ModelCapabilities:
    model_id:str
    providers:tuple[str,...]
    context_tokens:int
    max_output_tokens:int
    supports_tools:bool=False
    supports_json_schema:bool=False
    def __post_init__(self):
        if not self.model_id.strip() or not self.providers or self.context_tokens<1 or not 1<=self.max_output_tokens<=self.context_tokens: raise ValueError("invalid capability")
class CapabilityRegistry:
    def __init__(self): self._models={}
    def register(self,item):
        if item.model_id in self._models: raise ValueError("duplicate model")
        self._models[item.model_id]=item
    def select(self,*,tools=False,json_schema=False,min_context=1):
        return [m for m in self._models.values() if m.context_tokens>=min_context and (not tools or m.supports_tools) and (not json_schema or m.supports_json_schema)]

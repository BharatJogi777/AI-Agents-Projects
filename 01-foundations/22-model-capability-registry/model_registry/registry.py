from .contracts import ModelCapabilities

class CapabilityRegistry:
    """In-memory registry populated from verified provider metadata."""
    def __init__(self): self._models={}
    def register(self,item:ModelCapabilities):
        if not isinstance(item,ModelCapabilities): raise TypeError("item must be ModelCapabilities")
        if item.model_id in self._models: raise ValueError(f"duplicate model: {item.model_id}")
        self._models[item.model_id]=item
    def get(self,model_id:str)->ModelCapabilities:
        try: return self._models[model_id]
        except KeyError as exc: raise KeyError(f"unknown model: {model_id}") from exc
    def select(self,*,provider:str|None=None,tools:bool=False,json_schema:bool=False,vision:bool=False,streaming:bool=False,min_context:int=1)->list[ModelCapabilities]:
        if type(min_context) is not int or min_context<1: raise ValueError("min_context must be a positive integer")
        requirements=(tools,json_schema,vision,streaming)
        if any(type(v) is not bool for v in requirements): raise TypeError("capability filters must be booleans")
        matches=[]
        for model in self._models.values():
            if provider and provider not in model.providers: continue
            if tools and not model.supports_tools: continue
            if json_schema and not model.supports_json_schema: continue
            if vision and not model.supports_vision: continue
            if streaming and not model.supports_streaming: continue
            if model.context_tokens>=min_context: matches.append(model)
        return sorted(matches,key=lambda item:(-item.context_tokens,item.model_id))

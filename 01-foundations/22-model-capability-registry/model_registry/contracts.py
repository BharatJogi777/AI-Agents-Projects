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
        if not isinstance(self.model_id,str) or not self.model_id.strip(): raise ValueError("model_id required")
        if not self.providers or any(not isinstance(p,str) or not p.strip() for p in self.providers): raise ValueError("at least one valid provider required")
        if len(set(self.providers))!=len(self.providers): raise ValueError("providers must be unique")
        if type(self.context_tokens) is not int or self.context_tokens<1: raise ValueError("context_tokens must be positive")
        if type(self.max_output_tokens) is not int or not 1<=self.max_output_tokens<=self.context_tokens: raise ValueError("invalid token limits")
        for field in ("supports_tools","supports_json_schema","supports_vision","supports_streaming"):
            if type(getattr(self,field)) is not bool: raise TypeError(f"{field} must be boolean")

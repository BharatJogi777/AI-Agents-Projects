"""Route requests using deterministic rules first, then an injected LLM classifier."""
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Route:
    name:str
    confidence:float
    source:str

class RuleLLMRouter:
    def __init__(self,rules:dict[str,Callable[[str],bool]],llm_classifier:Callable[[str],str],allowed_routes:set[str]):
        if not allowed_routes or not set(rules).issubset(allowed_routes): raise ValueError("rules must target allowed routes")
        self.rules=rules; self.llm_classifier=llm_classifier; self.allowed=allowed_routes
    def route(self,text:str)->Route:
        if not text.strip(): raise ValueError("input cannot be empty")
        for name,rule in self.rules.items():
            if rule(text): return Route(name,1.0,"deterministic_rule")
        selected=self.llm_classifier(text)
        if not isinstance(selected,str) or selected not in self.allowed: raise ValueError("LLM selected an unknown route")
        return Route(selected,0.0,"llm_fallback")

from typing import Callable
from .contracts import Route
class RuleLLMRouter:
    """Apply ordered deterministic rules before invoking an allowlisted LLM fallback."""
    def __init__(self,rules:dict[str,Callable[[str],bool]],llm_classifier:Callable[[str],str],allowed_routes:set[str]):
        if not allowed_routes or any(not isinstance(x,str) or not x.strip() for x in allowed_routes): raise ValueError("allowed_routes must contain non-empty names")
        if not set(rules).issubset(allowed_routes): raise ValueError("rules must target allowed routes")
        if any(not callable(rule) for rule in rules.values()) or not callable(llm_classifier): raise TypeError("rules and classifier must be callable")
        self.rules=dict(rules); self.llm_classifier=llm_classifier; self.allowed=frozenset(allowed_routes)
    def route(self,text:str)->Route:
        if not isinstance(text,str) or not text.strip(): raise ValueError("input cannot be empty")
        for name,rule in self.rules.items():
            if rule(text): return Route(name,1.0,"deterministic_rule")
        selected=self.llm_classifier(text)
        if not isinstance(selected,str) or selected not in self.allowed: raise ValueError("LLM selected an unknown route")
        return Route(selected,0.0,"llm_fallback")

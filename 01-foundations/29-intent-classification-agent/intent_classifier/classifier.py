import math
from typing import Callable
from .contracts import IntentResult
class IntentClassifier:
    """Validate untrusted classifier output and apply a conservative review threshold."""
    def __init__(self,intents:set[str],classifier:Callable[[str],dict],threshold:float=.75,max_text_chars:int=20000):
        if not intents or any(not isinstance(x,str) or not x.strip() for x in intents): raise ValueError("intents must contain non-empty names")
        if isinstance(threshold,bool) or not isinstance(threshold,(int,float)) or not 0<=threshold<=1: raise ValueError("threshold must be 0..1")
        if type(max_text_chars) is not int or max_text_chars<1: raise ValueError("max_text_chars must be positive")
        if not callable(classifier): raise TypeError("classifier must be callable")
        self.intents=frozenset(intents); self.classifier=classifier; self.threshold=float(threshold); self.max_text_chars=max_text_chars
    def classify(self,text:str)->IntentResult:
        if not isinstance(text,str) or not text.strip(): raise ValueError("text cannot be empty")
        if len(text)>self.max_text_chars: raise ValueError("text exceeds configured length")
        raw=self.classifier(text)
        if not isinstance(raw,dict): raise ValueError("classifier must return an object")
        intent=raw.get("intent"); confidence=raw.get("confidence")
        if not isinstance(intent,str) or intent not in self.intents: raise ValueError("unknown intent")
        if isinstance(confidence,bool) or not isinstance(confidence,(int,float)) or not math.isfinite(confidence) or not 0<=confidence<=1: raise ValueError("confidence must be finite and 0..1")
        score=float(confidence)
        return IntentResult(intent,score,score<self.threshold)

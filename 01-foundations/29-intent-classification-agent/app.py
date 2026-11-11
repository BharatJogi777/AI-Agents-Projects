"""Validate intent classification results and support an injected classifier model."""
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class IntentResult:
    intent:str
    confidence:float
    needs_human_review:bool

class IntentClassifier:
    def __init__(self,intents:set[str],classifier:Callable[[str],dict],threshold:float=.75):
        if not intents or not 0<=threshold<=1: raise ValueError("invalid intents or threshold")
        self.intents=set(intents); self.classifier=classifier; self.threshold=threshold
    def classify(self,text:str)->IntentResult:
        if not text.strip(): raise ValueError("text cannot be empty")
        raw=self.classifier(text)
        if not isinstance(raw,dict): raise ValueError("classifier must return an object")
        intent=raw.get("intent"); confidence=raw.get("confidence")
        if intent not in self.intents: raise ValueError("unknown intent")
        if isinstance(confidence,bool) or not isinstance(confidence,(int,float)) or not 0<=confidence<=1: raise ValueError("confidence must be 0..1")
        score=float(confidence)
        return IntentResult(intent,score,score<self.threshold)

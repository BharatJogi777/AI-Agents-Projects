from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Intent:
    name: str
    confidence: float

@dataclass(frozen=True)
class Dispatch:
    specialist: str
    result: Any

class IntentRouter:
    def __init__(self, handlers: dict[str, Callable[[str], Any]], classify: Callable[[str], Intent], min_confidence: float = 0.7):
        if not handlers: raise ValueError("at least one handler is required")
        if not 0 <= min_confidence <= 1: raise ValueError("confidence threshold must be between zero and one")
        self.handlers, self.classify, self.threshold = dict(handlers), classify, min_confidence

    def run(self, text: str) -> Dispatch:
        if not text.strip(): raise ValueError("input text is required")
        intent = self.classify(text)
        if not isinstance(intent, Intent) or not 0 <= intent.confidence <= 1:
            raise ValueError("classifier returned invalid intent")
        if intent.confidence < self.threshold: raise LookupError("intent confidence below threshold")
        handler = self.handlers.get(intent.name)
        if handler is None: raise LookupError("no specialist registered for intent")
        return Dispatch(intent.name, handler(text))

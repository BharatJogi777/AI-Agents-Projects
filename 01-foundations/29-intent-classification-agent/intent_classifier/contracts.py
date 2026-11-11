from dataclasses import dataclass
@dataclass(frozen=True)
class IntentResult:
    intent:str
    confidence:float
    needs_human_review:bool

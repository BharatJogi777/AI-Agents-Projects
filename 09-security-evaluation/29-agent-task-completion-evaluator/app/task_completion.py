"""Score task completion against explicit required and prohibited outcomes."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CompletionReport:
    complete: bool
    completion_ratio: float
    missing_requirements: tuple[str,...]
    prohibited_outcomes: tuple[str,...]

def evaluate_completion(observed: set[str], required: set[str], prohibited: set[str] | None = None) -> CompletionReport:
    prohibited=prohibited or set()
    if not all(isinstance(s,set) for s in (observed,required,prohibited)):
        raise ValueError("observed, required, and prohibited must be sets")
    if any(not isinstance(x,str) or not x for x in observed|required|prohibited):
        raise ValueError("outcome labels must be non-empty strings")
    missing=required-observed; violations=observed&prohibited
    ratio=len(required & observed)/len(required) if required else 1.0
    return CompletionReport(not missing and not violations,ratio,tuple(sorted(missing)),tuple(sorted(violations)))

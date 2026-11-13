from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class ExpertScore:
    expert: str
    weight: float

@dataclass(frozen=True)
class ExpertResult:
    values: dict[str, Any]
    weights: dict[str, float]

class MixtureOfExperts:
    def __init__(self, experts: dict[str, Callable[[str], Any]], scorer: Callable[[str, tuple[str, ...]], list[ExpertScore]], top_k: int = 2):
        if not experts or top_k < 1:
            raise ValueError("experts and positive top_k required")
        self.experts, self.scorer, self.top_k = dict(experts), scorer, top_k

    def run(self, task: str) -> ExpertResult:
        if not task.strip():
            raise ValueError("task is required")
        scores = self.scorer(task, tuple(sorted(self.experts)))
        if not isinstance(scores, list) or not scores:
            raise ValueError("scorer must return expert scores")
        if len({s.expert for s in scores}) != len(scores):
            raise ValueError("duplicate expert score")
        for score in scores:
            if score.expert not in self.experts or not 0 <= score.weight <= 1:
                raise ValueError("invalid expert or routing weight")
        selected = sorted(scores, key=lambda s: (-s.weight, s.expert))[:self.top_k]
        total = sum(s.weight for s in selected)
        if total <= 0:
            raise ValueError("selected experts have zero total weight")
        weights = {s.expert: s.weight / total for s in selected}
        values = {name: self.experts[name](task) for name in weights}
        return ExpertResult(values, weights)

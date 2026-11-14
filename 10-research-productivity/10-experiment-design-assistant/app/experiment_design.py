"""Build a basic experiment outline; not a substitute for specialist review."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ExperimentPlan:
    question: str
    hypothesis: str
    groups: tuple[str,...]
    primary_outcome: str
    duration_days: int
    allocation_per_group: tuple[float,...]
    randomization_recommended: bool
    review_required: bool = True
def design_experiment(*, question: str, hypothesis: str, groups: list[str], primary_outcome: str, duration_days: int, allocation: list[float]|None=None) -> ExperimentPlan:
    for name,value in (("question",question),("hypothesis",hypothesis),("primary_outcome",primary_outcome)):
        if not isinstance(value,str) or not value.strip(): raise ValueError(f"{name} must be non-empty")
    if not isinstance(groups,list) or len(groups)<2 or any(not isinstance(g,str) or not g.strip() for g in groups): raise ValueError("at least two non-empty group names are required")
    if len(set(groups))!=len(groups): raise ValueError("group names must be unique")
    if not isinstance(duration_days,int) or isinstance(duration_days,bool) or duration_days<1: raise ValueError("duration_days must be a positive integer")
    weights=[1.0]*len(groups) if allocation is None else allocation
    if not isinstance(weights,list) or len(weights)!=len(groups) or any(not isinstance(w,(int,float)) or isinstance(w,bool) or w<=0 for w in weights): raise ValueError("allocation must contain one positive weight per group")
    total=sum(weights)
    ratios=tuple(round(w/total,6) for w in weights)
    return ExperimentPlan(question.strip(),hypothesis.strip(),tuple(g.strip() for g in groups),primary_outcome.strip(),duration_days,ratios,True)

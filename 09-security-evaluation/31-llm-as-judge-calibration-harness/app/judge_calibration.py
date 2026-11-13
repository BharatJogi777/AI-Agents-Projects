"""Calibrate a judge score against human reference labels."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CalibrationReport:
    count: int
    mean_absolute_error: float
    within_tolerance: int
    agreement_rate: float

def calibrate_judge(judge_scores: list[float], human_scores: list[float], *, tolerance: float = 0.1) -> CalibrationReport:
    if not isinstance(judge_scores,list) or not isinstance(human_scores,list) or len(judge_scores)!=len(human_scores) or not judge_scores:
        raise ValueError("score lists must be non-empty and equal length")
    if any(type(x) not in (int,float) or not 0 <= x <= 1 for x in judge_scores+human_scores):
        raise ValueError("scores must be numeric values in [0, 1]")
    if type(tolerance) not in (int,float) or not 0 <= tolerance <= 1: raise ValueError("tolerance must be in [0, 1]")
    errors=[abs(a-b) for a,b in zip(judge_scores,human_scores)]
    within=sum(e<=tolerance for e in errors)
    return CalibrationReport(len(errors),sum(errors)/len(errors),within,within/len(errors))

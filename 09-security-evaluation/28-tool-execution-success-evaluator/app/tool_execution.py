"""Summarize tool invocation outcomes without hiding failed attempts."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ExecutionReport:
    total: int
    succeeded: int
    failed: int
    success_rate: float
    failure_indices: tuple[int,...]

def evaluate_executions(outcomes: list[bool]) -> ExecutionReport:
    if not isinstance(outcomes,list) or any(type(x) is not bool for x in outcomes):
        raise ValueError("outcomes must be a list of booleans")
    total=len(outcomes); succeeded=sum(outcomes); failed=total-succeeded
    return ExecutionReport(total,succeeded,failed,succeeded/total if total else 0.0,
                           tuple(i for i,ok in enumerate(outcomes) if not ok))

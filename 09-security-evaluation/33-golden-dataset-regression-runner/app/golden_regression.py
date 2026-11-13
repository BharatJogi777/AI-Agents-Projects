"""Compare actual outputs with a versioned golden expectation set."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RegressionReport:
    total: int
    passed: int
    failed_ids: tuple[str,...]
    pass_rate: float

def run_regression(cases: list[dict[str,str]], actual: dict[str,str]) -> RegressionReport:
    if not isinstance(cases,list) or not isinstance(actual,dict): raise ValueError("cases and actual outputs must be list and dict")
    ids=[]
    for case in cases:
        if not isinstance(case,dict) or not isinstance(case.get("id"),str) or not case["id"] or not isinstance(case.get("expected"),str):
            raise ValueError("each case requires a non-empty id and string expected output")
        ids.append(case["id"])
    if len(set(ids)) != len(ids): raise ValueError("case IDs must be unique")
    if any(not isinstance(k,str) or not isinstance(v,str) for k,v in actual.items()): raise ValueError("actual outputs must map strings to strings")
    failed=tuple(cid for cid,case in zip(ids,cases) if actual.get(cid) != case["expected"])
    total=len(cases); passed=total-len(failed)
    return RegressionReport(total,passed,failed,passed/total if total else 1.0)

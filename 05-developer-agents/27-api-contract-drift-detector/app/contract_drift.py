"""Compare observed API operations against a declared contract."""
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Operation:
    method: str
    path: str

def normalize(operations: list[dict]) -> set[Operation]:
    result=set()
    for item in operations:
        method=str(item.get("method","")).upper().strip()
        path=str(item.get("path","")).strip()
        if not method or not path.startswith("/"): raise ValueError(f"Invalid operation: {item!r}")
        result.add(Operation(method,path))
    return result

def detect_drift(contract: list[dict], observed: list[dict]) -> dict[str,list[dict]]:
    expected, actual=normalize(contract),normalize(observed)
    return {
        "missing_from_runtime":[{"method":x.method,"path":x.path} for x in sorted(expected-actual)],
        "undocumented_runtime":[{"method":x.method,"path":x.path} for x in sorted(actual-expected)],
        "in_sync":[{"method":x.method,"path":x.path} for x in sorted(expected&actual)],
    }

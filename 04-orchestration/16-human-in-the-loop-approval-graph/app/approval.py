from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any

class Decision(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"

@dataclass(frozen=True)
class Approval:
    request_id: str
    decision: Decision
    reviewer: str
    comment: str = ""

@dataclass(frozen=True)
class ApprovalResult:
    status: str
    value: Any = None
    request_id: str = ""

class ApprovalGraph:
    def __init__(self, action: Callable[[], Any]):
        self.action = action
        self.pending: dict[str, ApprovalResult] = {}

    def request(self, request_id: str) -> ApprovalResult:
        if not request_id.strip(): raise ValueError("request_id required")
        if request_id in self.pending: return self.pending[request_id]
        result = ApprovalResult("pending", request_id=request_id)
        self.pending[request_id] = result
        return result

    def decide(self, approval: Approval) -> ApprovalResult:
        if not approval.reviewer.strip(): raise ValueError("reviewer required")
        current = self.pending.get(approval.request_id)
        if current is None: raise KeyError("unknown approval request")
        if current.status != "pending": raise RuntimeError("approval already decided")
        if approval.decision == Decision.REJECT:
            result = ApprovalResult("rejected", request_id=approval.request_id)
        elif approval.decision == Decision.APPROVE:
            result = ApprovalResult("approved", self.action(), approval.request_id)
        else: raise ValueError("unsupported decision")
        self.pending[approval.request_id] = result
        return result

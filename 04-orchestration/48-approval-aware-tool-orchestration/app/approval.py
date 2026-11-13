"""Gate sensitive tool calls behind explicit, single-use approvals."""
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Approval:
    approval_id: str
    tool_name: str
    requester: str

class ApprovalGate:
    def __init__(self):
        self._pending: dict[str, Approval] = {}

    def request(self, approval_id: str, tool_name: str, requester: str) -> Approval:
        if not all((approval_id, tool_name, requester)):
            raise ValueError("approval id, tool name, and requester are required")
        if approval_id in self._pending:
            raise ValueError("approval id already exists")
        approval = Approval(approval_id, tool_name, requester)
        self._pending[approval_id] = approval
        return approval

    def approve_and_execute(self, approval_id: str, tool_name: str,
                            executor: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        approval = self._pending.get(approval_id)
        if approval is None:
            raise PermissionError("approval is missing, expired, or already consumed")
        if approval.tool_name != tool_name:
            raise PermissionError("approval does not authorize this tool")
        del self._pending[approval_id]
        return executor(*args, **kwargs)

    def deny(self, approval_id: str) -> bool:
        return self._pending.pop(approval_id, None) is not None

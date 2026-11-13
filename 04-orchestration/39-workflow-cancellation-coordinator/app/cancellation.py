"""Cooperative workflow cancellation tokens and child propagation."""
from dataclasses import dataclass, field

@dataclass
class CancellationToken:
    workflow_id: str
    cancelled: bool = False
    reason: str | None = None
    children: list["CancellationToken"] = field(default_factory=list)

    def add_child(self, child: "CancellationToken") -> None:
        if child is self or child.workflow_id == self.workflow_id:
            raise ValueError("invalid child token")
        if self.cancelled:
            child.cancel(self.reason or "parent cancelled")
        self.children.append(child)

    def cancel(self, reason: str = "cancelled") -> None:
        if self.cancelled:
            return
        if not reason:
            raise ValueError("cancellation reason is required")
        self.cancelled, self.reason = True, reason
        for child in self.children:
            child.cancel(reason)

    def raise_if_cancelled(self) -> None:
        if self.cancelled:
            raise RuntimeError(f"workflow {self.workflow_id} cancelled: {self.reason}")

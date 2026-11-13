"""Role-constrained agent collaboration and contribution aggregation."""
from dataclasses import dataclass, field
from enum import Enum

class Phase(str, Enum):
    OPEN = "open"
    COMPLETE = "complete"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class Role:
    name: str
    required: bool = True

@dataclass
class Collaboration:
    roles: dict[str, Role]
    assignments: dict[str, str] = field(default_factory=dict)
    contributions: dict[str, dict] = field(default_factory=dict)
    phase: Phase = Phase.OPEN

    def assign(self, role_name: str, agent_id: str) -> None:
        self._ensure_open()
        if role_name not in self.roles:
            raise ValueError(f"unknown role: {role_name}")
        if not agent_id:
            raise ValueError("agent_id is required")
        if role_name in self.assignments:
            raise ValueError(f"role already assigned: {role_name}")
        self.assignments[role_name] = agent_id

    def contribute(self, role_name: str, agent_id: str, content: dict) -> None:
        self._ensure_open()
        if self.assignments.get(role_name) != agent_id:
            raise PermissionError("agent is not assigned to this role")
        if not isinstance(content, dict) or not content:
            raise ValueError("contribution must be a non-empty dictionary")
        self.contributions[role_name] = dict(content)

    def missing_roles(self) -> list[str]:
        return [name for name, role in self.roles.items()
                if role.required and name not in self.contributions]

    def complete(self) -> dict[str, dict]:
        self._ensure_open()
        if self.missing_roles():
            raise RuntimeError(f"required contributions missing: {self.missing_roles()}")
        self.phase = Phase.COMPLETE
        return dict(self.contributions)

    def cancel(self) -> None:
        self._ensure_open()
        self.phase = Phase.CANCELLED

    def _ensure_open(self) -> None:
        if self.phase != Phase.OPEN:
            raise RuntimeError(f"collaboration is {self.phase.value}")

"""Track estimated and actual agent spend against per-run budgets."""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Charge:
    agent_id: str
    amount: float
    category: str = "inference"

@dataclass
class BudgetManager:
    limit: float
    charges: list[Charge] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.limit < 0:
            raise ValueError("budget limit cannot be negative")

    @property
    def spent(self) -> float:
        return sum(c.amount for c in self.charges)

    @property
    def remaining(self) -> float:
        return max(0.0, self.limit - self.spent)

    @property
    def exceeded(self) -> bool:
        return self.spent > self.limit

    def authorize(self, agent_id: str, estimated_cost: float) -> bool:
        if not agent_id.strip() or estimated_cost < 0:
            raise ValueError("agent id and non-negative estimate are required")
        return estimated_cost <= self.remaining

    def record(self, charge: Charge) -> None:
        if not charge.agent_id.strip() or charge.amount < 0 or not charge.category.strip():
            raise ValueError("invalid charge")
        self.charges.append(charge)

    def report(self) -> dict[str, float | bool]:
        return {"limit": self.limit, "spent": self.spent,
                "remaining": self.remaining, "exceeded": self.exceeded}

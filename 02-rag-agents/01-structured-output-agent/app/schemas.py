from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Category(StrEnum):
    ENGINEERING = "engineering"
    OPERATIONS = "operations"
    CUSTOMER_SUPPORT = "customer_support"
    SECURITY = "security"
    OTHER = "other"


class ActionItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task: str = Field(min_length=3, max_length=240)
    owner: str | None = Field(default=None, max_length=80)
    due_date: str | None = Field(default=None, description="ISO-8601 date if explicitly present; otherwise null")


class TaskAnalysis(BaseModel):
    """Contract returned by the model. Unknown fields are rejected."""

    model_config = ConfigDict(extra="forbid")

    summary: str = Field(min_length=10, max_length=500)
    priority: Priority
    category: Category
    action_items: list[ActionItem] = Field(max_length=20)
    needs_human_review: bool
    uncertainty: str | None = Field(
        default=None,
        max_length=300,
        description="Explain missing or ambiguous information; null when there is no material uncertainty.",
    )

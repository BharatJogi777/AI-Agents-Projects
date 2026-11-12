from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


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
    """An action plus source quotes for every extracted factual field."""

    model_config = ConfigDict(extra="forbid")

    task: str = Field(min_length=3, max_length=240)
    evidence: str = Field(
        min_length=3,
        max_length=500,
        description="Verbatim substring from the user's request supporting this action.",
    )
    owner: str | None = Field(default=None, max_length=80)
    owner_evidence: str | None = Field(
        default=None,
        max_length=300,
        description="Verbatim source substring containing the owner; null when owner is unknown.",
    )
    due_date: str | None = Field(default=None, description="ISO-8601 date only when explicitly present.")
    due_date_evidence: str | None = Field(
        default=None,
        max_length=300,
        description="Verbatim source substring containing the due date; null when date is unknown.",
    )

    @model_validator(mode="after")
    def require_evidence_for_extracted_fields(self):
        if (self.owner is None) != (self.owner_evidence is None):
            raise ValueError("owner and owner_evidence must either both be present or both be null")
        if (self.due_date is None) != (self.due_date_evidence is None):
            raise ValueError("due_date and due_date_evidence must either both be present or both be null")
        return self


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

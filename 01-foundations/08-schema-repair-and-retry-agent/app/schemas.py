from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ActionItem(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    task: str = Field(min_length=3, max_length=240)
    owner: str | None = Field(default=None, max_length=80)


class TaskReport(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    summary: str = Field(min_length=10, max_length=400)
    priority: Priority
    action_items: list[ActionItem] = Field(max_length=15)
    needs_human_review: bool

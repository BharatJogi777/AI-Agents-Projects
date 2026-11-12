from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class ConversationCreate(StrictModel):
    system_prompt: str = Field(min_length=1, max_length=8000)
    max_turns: int = Field(default=10, ge=1, le=500)

class MessageCreate(StrictModel):
    content: str = Field(min_length=1, max_length=8000)

class MessageResponse(StrictModel):
    id: int
    conversation_id: str
    role: Literal["user", "assistant"]
    content: str
    created_at: str

class ConversationResponse(StrictModel):
    id: str
    system_prompt: str
    max_turns: int
    created_at: str
    updated_at: str

class ConversationListItem(ConversationResponse):
    message_count: int

class HistoryResponse(StrictModel):
    conversation_id: str
    system_prompt: str
    messages: list[MessageResponse]
    limit: int
    offset: int

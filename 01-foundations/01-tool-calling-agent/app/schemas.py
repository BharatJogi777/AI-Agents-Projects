from pydantic import BaseModel, ConfigDict, Field
class RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1, max_length=8000)
class RunResponse(BaseModel):
    answer: str

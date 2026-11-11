from collections.abc import Callable

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.agent import AgentStepLimitError, ToolCallingAgent


class AgentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1, max_length=8000)


class AgentResponse(BaseModel):
    answer: str


def create_app(
    agent: ToolCallingAgent,
    readiness_check: Callable[[], bool] | None = None,
) -> FastAPI:
    app = FastAPI(title="Tool-calling Agent API", version="0.3.0")

    @app.get("/health/live")
    def liveness() -> dict[str, str]:
        # Liveness answers only whether this process can serve HTTP.
        return {"status": "alive"}

    @app.get("/health/ready")
    def readiness() -> dict[str, str]:
        # Readiness is dependency-aware; it does not run a model completion.
        if readiness_check is not None and not readiness_check():
            raise HTTPException(status_code=503, detail="LLM provider is not ready")
        return {"status": "ready"}

    @app.post("/v1/agent/run", response_model=AgentResponse)
    def run_agent(request: AgentRequest) -> AgentResponse:
        try:
            return AgentResponse(answer=agent.run(request.prompt))
        except AgentStepLimitError as exc:
            raise HTTPException(status_code=429, detail="Agent step budget exhausted") from exc
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=502, detail="Agent execution failed") from exc

    return app

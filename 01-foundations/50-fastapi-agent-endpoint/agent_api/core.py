import inspect
from collections.abc import Callable
from fastapi import FastAPI,HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel,ConfigDict,Field,StrictStr
class AgentRequest(BaseModel):
 model_config=ConfigDict(extra="forbid",str_strip_whitespace=True)
 prompt:StrictStr=Field(min_length=1,max_length=4000)
class AgentResponse(BaseModel):result:StrictStr
class HealthResponse(BaseModel):status:StrictStr
Agent=Callable[[str],object]
def create_app(agent:Agent)->FastAPI:
 if not callable(agent):raise TypeError("agent must be callable")
 app=FastAPI(title="Agent API",version="1.0.0");app.state.agent=agent
 @app.get("/health",response_model=HealthResponse)
 @app.get("/health/live",response_model=HealthResponse)
 async def liveness():return HealthResponse(status="ok")
 @app.get("/health/ready",response_model=HealthResponse)
 async def readiness():return HealthResponse(status="ready")
 @app.post("/runs",response_model=AgentResponse)
 async def create_run(request:AgentRequest):
  try:
   if inspect.iscoroutinefunction(agent):result=await agent(request.prompt)
   else:
    result=await run_in_threadpool(agent,request.prompt)
    if inspect.isawaitable(result):result=await result
  except Exception as exc:raise HTTPException(status_code=502,detail="agent execution failed") from exc
  if not isinstance(result,str):raise HTTPException(status_code=502,detail="agent returned an invalid response")
  return AgentResponse(result=result)
 return app

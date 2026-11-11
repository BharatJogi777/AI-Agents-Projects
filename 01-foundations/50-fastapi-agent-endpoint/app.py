"""AG-050: FastAPI agent endpoint. Expose an injected agent with strict Pydantic request validation, bounded prompt size, health check, and sanitized execution errors."""
from collections.abc import Callable
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,ConfigDict,Field
class AgentRequest(BaseModel):
 model_config=ConfigDict(extra="forbid")
 prompt:str=Field(min_length=1,max_length=4000)
class AgentResponse(BaseModel): result:str
Agent=Callable[[str],str]
def create_app(agent:Agent)->FastAPI:
 if not callable(agent): raise TypeError("agent must be callable")
 app=FastAPI(title="Agent API",version="1.0.0")
 @app.get("/health")
 def health(): return {"status":"ok"}
 @app.post("/runs",response_model=AgentResponse)
 def create_run(request:AgentRequest):
  try: result=agent(request.prompt)
  except Exception as exc: raise HTTPException(status_code=502,detail="agent execution failed") from exc
  if not isinstance(result,str): raise HTTPException(status_code=502,detail="invalid agent response")
  return AgentResponse(result=result)
 return app
app=create_app(lambda prompt:f"Received task: {prompt}")

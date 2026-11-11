import json
from datetime import datetime, timezone
from typing import Any, Protocol
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class AddArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    a: float
    b: float

class TextArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    text: str = Field(min_length=1, max_length=2000)

class EmptyArgs(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

def _tools():
    return {
      "add_numbers": (AddArgs, lambda x: {"sum": x.a+x.b}, "Add two numbers."),
      "text_length": (TextArgs, lambda x: {"length": len(x.text)}, "Count characters in text."),
      "current_utc_time": (EmptyArgs, lambda _: {"utc": datetime.now(timezone.utc).isoformat()}, "Return current UTC time.")
    }

class ChatClient(Protocol):
    def chat(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]: ...

class MultiToolAgent:
    def __init__(self, client: ChatClient, max_steps: int=4):
        if not 1 <= max_steps <= 8: raise ValueError("max_steps must be 1..8")
        self.client, self.max_steps, self.tools = client, max_steps, _tools()

    def run(self, prompt: str) -> str:
        if not isinstance(prompt,str) or not prompt.strip(): raise ValueError("prompt cannot be empty")
        defs=[{"type":"function","function":{"name":n,"description":d,"parameters":s.model_json_schema()}} for n,(s,_,d) in self.tools.items()]
        messages=[{"role":"system","content":"Select the appropriate available tool. Never invent tool results. Explain results concisely."},{"role":"user","content":prompt}]
        for _ in range(self.max_steps):
            response=self.client.chat(messages,defs)
            msg=response.get("message") if isinstance(response,dict) else None
            if not isinstance(msg,dict): raise RuntimeError("Malformed model response")
            calls=msg.get("tool_calls") or []
            if not calls:
                answer=msg.get("content")
                if not isinstance(answer,str) or not answer.strip(): raise RuntimeError("Empty model answer")
                return answer
            messages.append(msg)
            for call in calls:
                name="unknown"
                try:
                    fn=call["function"]; name=fn["name"]
                    if name not in self.tools: raise ValueError("Tool is not allowlisted")
                    schema,handler,_=self.tools[name]
                    raw=fn.get("arguments",{})
                    args=json.loads(raw) if isinstance(raw,str) else raw
                    result={"ok":True,"result":handler(schema.model_validate(args))}
                except (KeyError,TypeError,ValueError,ValidationError,json.JSONDecodeError) as exc:
                    result={"ok":False,"error":str(exc)[:400]}
                messages.append({"role":"tool","tool_name":name,"content":json.dumps(result)})
        raise RuntimeError(f"Agent exceeded {self.max_steps} steps")

class OllamaClient:
    def __init__(self, model="qwen3:4b", base_url="http://localhost:11434", timeout=60):
        import httpx
        self.httpx,self.model,self.url,self.timeout=httpx,model,base_url.rstrip("/"),timeout
    def chat(self,messages,tools):
        r=self.httpx.post(self.url+"/api/chat",json={"model":self.model,"messages":messages,"tools":tools,"stream":False},timeout=self.timeout)
        r.raise_for_status()
        data=r.json()
        if not isinstance(data,dict) or not isinstance(data.get("message"),dict): raise RuntimeError("Invalid Ollama response")
        return data

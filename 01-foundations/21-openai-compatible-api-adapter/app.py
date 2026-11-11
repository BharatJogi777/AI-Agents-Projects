"""OpenAI-compatible chat-completions adapter."""
import httpx
from dataclasses import dataclass,field

@dataclass(frozen=True)
class Message:
    role:str
    content:str
    def __post_init__(self):
        if self.role not in {"system","user","assistant"}: raise ValueError("unsupported role")
        if not isinstance(self.content,str): raise TypeError("content must be text")

@dataclass(frozen=True)
class Request:
    model:str
    messages:tuple[Message,...]
    temperature:float=0.0
    max_tokens:int=512
    def __post_init__(self):
        if not self.model.strip() or not self.messages: raise ValueError("model and messages required")
        if not 0<=self.temperature<=2 or not 1<=self.max_tokens<=32768: raise ValueError("invalid generation limits")

@dataclass(frozen=True)
class Response:
    content:str
    model:str
    finish_reason:str|None=None
    usage:dict[str,int]=field(default_factory=dict)

class ProviderError(RuntimeError): pass

class OpenAICompatibleProvider:
    def __init__(self,base_url:str,api_key:str|None=None,timeout:float=60,transport:httpx.BaseTransport|None=None):
        if not base_url.startswith(("http://","https://")): raise ValueError("base_url must be HTTP(S)")
        if not 0<timeout<=600: raise ValueError("timeout must be in (0,600]")
        self.base_url=base_url.rstrip("/"); self.api_key=api_key; self.timeout=timeout; self.transport=transport
    def chat(self,request:Request)->Response:
        headers={"Authorization":f"Bearer {self.api_key}"} if self.api_key else {}
        body={"model":request.model,"messages":[{"role":m.role,"content":m.content} for m in request.messages],
              "temperature":request.temperature,"max_tokens":request.max_tokens,"stream":False}
        try:
            with httpx.Client(timeout=self.timeout,transport=self.transport) as client:
                response=client.post(self.base_url+"/chat/completions",headers=headers,json=body)
                response.raise_for_status(); payload=response.json()
        except (httpx.HTTPError,ValueError) as exc: raise ProviderError("chat completion request failed") from exc
        try:
            choice=payload["choices"][0]; content=choice["message"]["content"]; model=payload.get("model",request.model)
            if not isinstance(content,str) or not isinstance(model,str): raise TypeError()
            usage={}
            for src,dst in (("prompt_tokens","input_tokens"),("completion_tokens","output_tokens")):
                n=payload.get("usage",{}).get(src)
                if isinstance(n,int) and n>=0: usage[dst]=n
            return Response(content,model,choice.get("finish_reason"),usage)
        except (KeyError,IndexError,TypeError,AttributeError) as exc:
            raise ProviderError("provider returned an invalid chat completion") from exc

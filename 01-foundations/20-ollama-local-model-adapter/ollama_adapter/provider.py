from typing import Any
import httpx
from contracts import ChatRequest,ChatResponse

class OllamaProviderError(RuntimeError): pass

class OllamaProvider:
    """Connection-pooled, non-streaming Ollama text-chat adapter."""
    def __init__(self,base_url:str="http://localhost:11434",timeout_seconds:float=60.0,
                 transport:httpx.BaseTransport|None=None,http_client:httpx.Client|None=None):
        if not base_url.startswith(("http://","https://")): raise ValueError("base_url must be HTTP(S)")
        if not 0<timeout_seconds<=600: raise ValueError("timeout_seconds must be in (0, 600]")
        if transport is not None and http_client is not None: raise ValueError("provide transport or http_client, not both")
        self.base_url=base_url.rstrip("/"); self.timeout_seconds=timeout_seconds
        self._owns_client=http_client is None
        self._client=http_client or httpx.Client(base_url=self.base_url,timeout=httpx.Timeout(timeout_seconds),transport=transport,
                                                 limits=httpx.Limits(max_connections=20,max_keepalive_connections=10))
    def close(self)->None:
        if self._owns_client: self._client.close()
    def __enter__(self): return self
    def __exit__(self,*_): self.close()
    def _json(self,method:str,path:str,**kwargs)->dict[str,Any]:
        try:
            response=self._client.request(method,path,**kwargs); response.raise_for_status()
            payload=response.json()
        except (httpx.HTTPError,ValueError) as exc:
            raise OllamaProviderError(f"Ollama {path} request failed") from exc
        if not isinstance(payload,dict): raise OllamaProviderError(f"Ollama {path} returned an invalid response")
        return payload
    def health(self)->bool:
        payload=self._json("GET","/api/tags")
        if not isinstance(payload.get("models"),list): raise OllamaProviderError("Ollama returned an invalid model list")
        return True
    def list_models(self)->list[dict[str,Any]]:
        payload=self._json("GET","/api/tags"); models=payload.get("models")
        if not isinstance(models,list) or any(not isinstance(item,dict) for item in models):
            raise OllamaProviderError("Ollama returned an invalid model list")
        return models
    def chat(self,request:ChatRequest)->ChatResponse:
        body={"model":request.model,"messages":[{"role":m.role,"content":m.content} for m in request.messages],
              "stream":False,"options":{"temperature":request.temperature,"num_predict":request.max_tokens}}
        payload=self._json("POST","/api/chat",json=body)
        message=payload.get("message"); content=message.get("content") if isinstance(message,dict) else None
        model=payload.get("model",request.model)
        if not isinstance(content,str) or not isinstance(model,str) or not model.strip():
            raise OllamaProviderError("Ollama returned an invalid chat response")
        done=payload.get("done")
        if done is not None and not isinstance(done,bool): raise OllamaProviderError("Ollama returned an invalid completion flag")
        usage={}
        for source,target in (("prompt_eval_count","input_tokens"),("eval_count","output_tokens")):
            value=payload.get(source)
            if value is not None:
                if type(value) is not int or value<0: raise OllamaProviderError("Ollama returned invalid token usage")
                usage[target]=value
        return ChatResponse(content=content,model=model,finish_reason="stop" if done is True else None,
                            usage=usage,raw={"done":done})

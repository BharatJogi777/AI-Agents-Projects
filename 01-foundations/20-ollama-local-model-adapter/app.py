"""Concrete Ollama adapter implementing the provider-neutral text chat contract."""
from typing import Any
import httpx
from contracts import ChatRequest,ChatResponse


class OllamaProviderError(RuntimeError): pass


class OllamaProvider:
    def __init__(self,base_url:str="http://localhost:11434",timeout_seconds:float=60.0,
                 transport:httpx.BaseTransport|None=None):
        if not base_url.startswith(("http://","https://")): raise ValueError("base_url must be HTTP(S)")
        if not 0<timeout_seconds<=600: raise ValueError("timeout_seconds must be in (0, 600]")
        self.base_url=base_url.rstrip("/")
        self.timeout_seconds=timeout_seconds
        self._transport=transport

    def _client(self):
        return httpx.Client(base_url=self.base_url,timeout=self.timeout_seconds,transport=self._transport)

    def health(self)->bool:
        try:
            with self._client() as client:
                response=client.get("/api/tags")
                response.raise_for_status()
                payload=response.json()
                return isinstance(payload,dict) and isinstance(payload.get("models"),list)
        except (httpx.HTTPError,ValueError) as exc:
            raise OllamaProviderError("Ollama health check failed") from exc

    def list_models(self)->list[dict[str,Any]]:
        try:
            with self._client() as client:
                response=client.get("/api/tags")
                response.raise_for_status()
                payload=response.json()
                models=payload.get("models") if isinstance(payload,dict) else None
                if not isinstance(models,list): raise OllamaProviderError("invalid /api/tags response")
                return models
        except httpx.HTTPError as exc:
            raise OllamaProviderError("Ollama model listing failed") from exc

    def chat(self,request:ChatRequest)->ChatResponse:
        body={
            "model":request.model,
            "messages":[{"role":m.role,"content":m.content} for m in request.messages],
            "stream":False,
            "options":{"temperature":request.temperature,"num_predict":request.max_tokens}
        }
        try:
            with self._client() as client:
                response=client.post("/api/chat",json=body)
                response.raise_for_status()
                payload=response.json()
        except (httpx.HTTPError,ValueError) as exc:
            raise OllamaProviderError("Ollama chat request failed") from exc
        message=payload.get("message") if isinstance(payload,dict) else None
        content=message.get("content") if isinstance(message,dict) else None
        model=payload.get("model",request.model) if isinstance(payload,dict) else request.model
        if not isinstance(content,str) or not isinstance(model,str):
            raise OllamaProviderError("Ollama returned an invalid chat response")
        usage={}
        if isinstance(payload,dict):
            for source,target in (("prompt_eval_count","input_tokens"),("eval_count","output_tokens")):
                value=payload.get(source)
                if isinstance(value,int) and value>=0: usage[target]=value
        return ChatResponse(content=content,model=model,
                            finish_reason="stop" if payload.get("done") else None,
                            usage=usage,raw={"done":payload.get("done")})

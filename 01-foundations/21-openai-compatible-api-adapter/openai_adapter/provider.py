import httpx
from .contracts import Request,Response

class ProviderError(RuntimeError): pass

class OpenAICompatibleProvider:
    """Connection-pooled adapter for OpenAI-compatible non-streaming chat APIs."""
    def __init__(self,base_url:str,api_key:str|None=None,timeout:float=60,
                 transport:httpx.BaseTransport|None=None,http_client:httpx.Client|None=None):
        if not base_url.startswith(("http://","https://")): raise ValueError("base_url must be HTTP(S)")
        if not 0<timeout<=600: raise ValueError("timeout must be in (0,600]")
        if transport is not None and http_client is not None: raise ValueError("provide transport or http_client, not both")
        self.api_key=api_key; self._owns_client=http_client is None
        self._client=http_client or httpx.Client(base_url=base_url.rstrip("/")+"/",timeout=httpx.Timeout(timeout),transport=transport,
                                                 limits=httpx.Limits(max_connections=20,max_keepalive_connections=10))
    def close(self):
        if self._owns_client: self._client.close()
    def __enter__(self): return self
    def __exit__(self,*_): self.close()
    def chat(self,request:Request)->Response:
        headers={"Authorization":f"Bearer {self.api_key}"} if self.api_key else {}
        body={"model":request.model,"messages":[{"role":m.role,"content":m.content} for m in request.messages],
              "temperature":request.temperature,"max_tokens":request.max_tokens,"stream":False}
        try:
            response=self._client.post("chat/completions",headers=headers,json=body); response.raise_for_status()
            payload=response.json()
        except (httpx.HTTPError,ValueError) as exc: raise ProviderError("chat completion request failed") from exc
        try:
            choices=payload["choices"]
            if not isinstance(choices,list) or not choices: raise ValueError()
            choice=choices[0]; message=choice["message"]; content=message["content"]
            model=payload.get("model",request.model); reason=choice.get("finish_reason")
            if not isinstance(content,str) or not isinstance(model,str) or not model.strip(): raise ValueError()
            if reason is not None and not isinstance(reason,str): raise ValueError()
            raw_usage=payload.get("usage") or {}
            if not isinstance(raw_usage,dict): raise ValueError()
            usage={}
            for src,dst in (("prompt_tokens","input_tokens"),("completion_tokens","output_tokens")):
                n=raw_usage.get(src)
                if n is not None:
                    if type(n) is not int or n<0: raise ValueError()
                    usage[dst]=n
            return Response(content,model,reason,usage)
        except (KeyError,IndexError,TypeError,ValueError,AttributeError) as exc:
            raise ProviderError("provider returned an invalid chat completion") from exc

import httpx
import pytest
from app import OllamaProvider,OllamaProviderError
from contracts import ChatMessage,ChatRequest


def request():
    return ChatRequest((ChatMessage("user","Hello"),),"qwen3:4b",temperature=.2,max_tokens=80)


def provider(handler):
    return OllamaProvider(transport=httpx.MockTransport(handler))


def test_chat_maps_request_and_response():
    def handle(req):
        body=__import__("json").loads(req.content)
        assert req.url.path=="/api/chat"
        assert body["model"]=="qwen3:4b" and body["stream"] is False
        assert body["messages"]==[{"role":"user","content":"Hello"}]
        return httpx.Response(200,json={"model":"qwen3:4b","message":{"content":"Hi"},"done":True,"prompt_eval_count":4,"eval_count":2})
    result=provider(handle).chat(request())
    assert result.content=="Hi" and result.finish_reason=="stop"
    assert result.usage=={"input_tokens":4,"output_tokens":2}


def test_health_and_model_listing():
    def handle(req): return httpx.Response(200,json={"models":[{"name":"qwen3:4b"}]})
    p=provider(handle)
    assert p.health() is True
    assert p.list_models()==[{"name":"qwen3:4b"}]


def test_http_failure_is_wrapped():
    p=provider(lambda req:httpx.Response(503,json={"error":"unavailable"}))
    with pytest.raises(OllamaProviderError,match="chat request failed"): p.chat(request())


def test_malformed_provider_response_is_rejected():
    p=provider(lambda req:httpx.Response(200,json={"message":{}}))
    with pytest.raises(OllamaProviderError,match="invalid chat response"): p.chat(request())


def test_invalid_configuration():
    with pytest.raises(ValueError): OllamaProvider("file:///tmp")
    with pytest.raises(ValueError): OllamaProvider(timeout_seconds=0)

import json
import httpx
import pytest
from app import OllamaProvider
from contracts import ChatMessage, ChatRequest
from ollama_adapter.provider import (OllamaAuthenticationError, OllamaInvalidRequest,
    OllamaRateLimited, OllamaResponseError, OllamaTimeout, OllamaUnavailable)

def request():
    return ChatRequest((ChatMessage("user", "Hello"),), "qwen3:4b", temperature=0.2, max_tokens=80)

def provider(handler, **kwargs):
    return OllamaProvider(transport=httpx.MockTransport(handler), **kwargs)

def test_chat_maps_request_and_response():
    def handle(req):
        body = json.loads(req.content)
        assert req.url.path == "/api/chat"
        assert body["model"] == "qwen3:4b" and body["stream"] is False
        assert body["messages"] == [{"role": "user", "content": "Hello"}]
        assert body["options"] == {"temperature": 0.2, "num_predict": 80}
        return httpx.Response(200, json={"model": "qwen3:4b", "message": {"content": "Hi"},
            "done": True, "done_reason": "stop", "prompt_eval_count": 4, "eval_count": 2,
            "total_duration": 123})
    with provider(handle) as p:
        result = p.chat(request())
    assert result.content == "Hi" and result.finish_reason == "stop"
    assert result.usage == {"input_tokens": 4, "output_tokens": 2}
    assert result.raw == {"done": True, "done_reason": "stop"}

def test_health_and_model_listing():
    p = provider(lambda req: httpx.Response(200, json={"models": [{"name": "qwen3:4b"}]}))
    assert p.health() is True
    assert p.list_models() == [{"name": "qwen3:4b"}]
    p.close()

@pytest.mark.parametrize("status,error", [(401, OllamaAuthenticationError), (403, OllamaAuthenticationError),
    (400, OllamaInvalidRequest), (404, OllamaInvalidRequest), (429, OllamaRateLimited),
    (503, OllamaUnavailable)])
def test_http_status_is_normalized(status, error):
    p = provider(lambda req: httpx.Response(status, text="sensitive provider body"))
    with pytest.raises(error):
        p.chat(request())

def test_rate_limit_exposes_retry_after_without_body():
    p = provider(lambda req: httpx.Response(429, headers={"Retry-After": "2.5"}, text="secret"))
    with pytest.raises(OllamaRateLimited) as caught:
        p.chat(request())
    assert caught.value.retry_after == 2.5
    assert "secret" not in str(caught.value)

def test_timeout_and_network_errors_are_normalized():
    def timeout(req): raise httpx.ReadTimeout("private detail")
    with pytest.raises(OllamaTimeout): provider(timeout).chat(request())
    def network(req): raise httpx.ConnectError("private detail")
    with pytest.raises(OllamaUnavailable): provider(network).chat(request())

@pytest.mark.parametrize("payload", [[], {"message": {}}, {"message": {"content": 123}},
    {"message": {"content": "ok"}, "model": ""}, {"message": {"content": "ok"}, "done": "yes"},
    {"message": {"content": "ok"}, "eval_count": -1},
    {"message": {"content": "ok"}, "eval_count": True},
    {"message": {"content": "ok"}, "done_reason": 4}])
def test_malformed_provider_response_is_rejected(payload):
    p = provider(lambda req: httpx.Response(200, json=payload))
    with pytest.raises(OllamaResponseError): p.chat(request())

def test_invalid_json_and_oversized_body_are_rejected():
    p = provider(lambda req: httpx.Response(200, content=b"{not-json"))
    with pytest.raises(OllamaResponseError, match="invalid JSON"): p.chat(request())
    p = provider(lambda req: httpx.Response(200, content=b"x" * 2048), max_response_bytes=1024)
    with pytest.raises(OllamaResponseError, match="exceeded"): p.chat(request())

def test_invalid_model_list_is_rejected():
    p = provider(lambda req: httpx.Response(200, json={"models": [None]}))
    with pytest.raises(OllamaResponseError): p.list_models()

def test_configuration_validation():
    for value in ("file:///tmp", "http://user:pass@localhost:11434",
                  "http://localhost:11434/path", "http://localhost:99999"):
        with pytest.raises(ValueError): OllamaProvider(base_url=value)
    with pytest.raises(ValueError): OllamaProvider(timeout_seconds=0)
    with pytest.raises(ValueError): OllamaProvider(max_response_bytes=100)

def test_injected_client_remains_caller_owned():
    client = httpx.Client(transport=httpx.MockTransport(
        lambda req: httpx.Response(200, json={"models": []})))
    p = OllamaProvider(http_client=client)
    p.close()
    assert not client.is_closed
    client.close()

def test_provider_rejects_calls_after_close():
    p = provider(lambda req: httpx.Response(200, json={"models": []}))
    p.close()
    with pytest.raises(RuntimeError, match="closed"): p.health()

def test_chat_requires_expected_request_type():
    p = provider(lambda req: httpx.Response(200, json={}))
    with pytest.raises(TypeError): p.chat(object())

def test_contract_rejects_non_finite_temperature_and_bool_token_limit():
    with pytest.raises(ValueError): ChatRequest((ChatMessage("user", "x"),), "model", float("nan"))
    with pytest.raises(ValueError): ChatRequest((ChatMessage("user", "x"),), "model", max_tokens=True)
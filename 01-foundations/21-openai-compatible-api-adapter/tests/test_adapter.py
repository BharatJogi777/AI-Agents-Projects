import json
import httpx
import pytest

from app import Message, Request, OpenAICompatibleProvider, ProviderError
from openai_adapter.provider import (
    ProviderAuthenticationError, ProviderInvalidRequest, ProviderRateLimited,
    ProviderResponseError, ProviderTimeout, ProviderUnavailable,
)

def req():
    return Request("test-model", (Message("user", "Hi"),), 0.1, 100)

def provider(handler, **kwargs):
    return OpenAICompatibleProvider("https://example.test/v1", transport=httpx.MockTransport(handler), **kwargs)

def test_mapping_auth_and_usage():
    def handler(r):
        assert r.url.path == "/v1/chat/completions"
        assert r.headers["authorization"] == "Bearer secret"
        body = json.loads(r.content)
        assert body["messages"] == [{"role": "user", "content": "Hi"}]
        assert body["stream"] is False and body["max_tokens"] == 100
        return httpx.Response(200, json={
            "model": "served-model",
            "choices": [{"message": {"role": "assistant", "content": "Hello"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 4, "completion_tokens": 2},
        })
    with OpenAICompatibleProvider("https://example.test/v1", "secret",
                                  transport=httpx.MockTransport(handler)) as p:
        out = p.chat(req())
    assert (out.content, out.model, out.finish_reason) == ("Hello", "served-model", "stop")
    assert out.usage == {"input_tokens": 4, "output_tokens": 2}

@pytest.mark.parametrize("status,error", [
    (401, ProviderAuthenticationError), (403, ProviderAuthenticationError),
    (400, ProviderInvalidRequest), (404, ProviderInvalidRequest),
    (429, ProviderRateLimited), (503, ProviderUnavailable),
])
def test_http_status_mapping(status, error):
    p = provider(lambda r: httpx.Response(status, text="sensitive response body"))
    with pytest.raises(error) as caught:
        p.chat(req())
    assert "sensitive response body" not in str(caught.value)

def test_retry_after_is_exposed():
    p = provider(lambda r: httpx.Response(429, headers={"Retry-After": "3"}))
    with pytest.raises(ProviderRateLimited) as caught:
        p.chat(req())
    assert caught.value.retry_after == 3.0

def test_timeout_and_network_errors_are_normalized():
    def timeout(r): raise httpx.ReadTimeout("private detail")
    with pytest.raises(ProviderTimeout):
        provider(timeout).chat(req())
    def network(r): raise httpx.ConnectError("private detail")
    with pytest.raises(ProviderUnavailable):
        provider(network).chat(req())

@pytest.mark.parametrize("payload", [
    [],
    {"choices": []},
    {"choices": [None]},
    {"choices": [{"message": {}}]},
    {"choices": [{"message": {"content": 3}}]},
    {"choices": [{"message": {"content": "ok"}, "finish_reason": 4}]},
    {"choices": [{"message": {"content": "ok"}}], "model": ""},
    {"choices": [{"message": {"content": "ok"}}], "usage": []},
    {"choices": [{"message": {"content": "ok"}}], "usage": {"prompt_tokens": -1}},
    {"choices": [{"message": {"content": "ok"}}], "usage": {"completion_tokens": True}},
])
def test_invalid_response_shapes(payload):
    p = provider(lambda r: httpx.Response(200, json=payload))
    with pytest.raises(ProviderResponseError):
        p.chat(req())

def test_invalid_json_and_oversized_body():
    p = provider(lambda r: httpx.Response(200, content=b"not-json"))
    with pytest.raises(ProviderResponseError, match="invalid JSON"):
        p.chat(req())
    p = provider(lambda r: httpx.Response(200, content=b"x" * 2048), max_response_bytes=1024)
    with pytest.raises(ProviderResponseError, match="size limit"):
        p.chat(req())

def test_missing_usage_is_allowed_for_compatible_servers():
    p = provider(lambda r: httpx.Response(200, json={
        "choices": [{"message": {"content": "ok"}, "finish_reason": None}]
    }))
    result = p.chat(req())
    assert result.content == "ok" and result.usage == {}

def test_request_and_configuration_validation():
    with pytest.raises(ValueError):
        Request("", (Message("user", "x"),))
    with pytest.raises(ValueError):
        Message("tool", "x")
    with pytest.raises(ValueError):
        Request("m", (Message("user", "x"),), float("nan"))
    with pytest.raises(ValueError):
        Request("m", (Message("user", "x"),), max_tokens=True)
    for url in ("file:///tmp", "https://user:pass@example.test/v1", "https://example.test/v1?key=x",
                "https://example.test:99999/v1"):
        with pytest.raises(ValueError):
            OpenAICompatibleProvider(url)
    with pytest.raises(ValueError):
        OpenAICompatibleProvider("https://example.test", api_key="bad\nheader")
    with pytest.raises(ValueError):
        OpenAICompatibleProvider("https://example.test", timeout=0)

def test_injected_http_client_remains_caller_owned():
    client = httpx.Client(transport=httpx.MockTransport(
        lambda r: httpx.Response(200, json={"choices": [{"message": {"content": "ok"}}]})
    ))
    p = OpenAICompatibleProvider("https://example.test/v1", http_client=client)
    p.close()
    assert not client.is_closed
    client.close()

def test_provider_rejects_calls_after_close():
    p = provider(lambda r: httpx.Response(200, json={}))
    p.close()
    with pytest.raises(RuntimeError, match="closed"):
        p.chat(req())

def test_chat_rejects_wrong_request_type():
    p = provider(lambda r: httpx.Response(200, json={}))
    with pytest.raises(TypeError):
        p.chat(object())

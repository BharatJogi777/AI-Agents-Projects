import httpx
import pytest

from app.llm import OllamaClient


def make_client(handler):
    http = httpx.Client(transport=httpx.MockTransport(handler))
    return OllamaClient("http://ollama.test", "qwen3:4b", http_client=http), http


def test_sends_schema_constrained_request():
    def handler(request):
        assert request.url.path == "/api/chat"
        payload = __import__("json").loads(request.read())
        assert payload["format"] == {"type": "object"}
        assert payload["options"]["temperature"] == 0
        return httpx.Response(200, json={"message": {"content": '{"ok":true}'}})

    client, http = make_client(handler)
    try:
        assert client.generate_structured([], {"type": "object"}) == '{"ok":true}'
    finally:
        http.close()


def test_http_error_is_sanitized():
    client, http = make_client(
        lambda request: httpx.Response(500, text="private diagnostics")
    )
    try:
        with pytest.raises(RuntimeError, match="HTTP 500") as error:
            client.generate_structured([], {})
        assert "private diagnostics" not in str(error.value)
    finally:
        http.close()


def test_invalid_provider_response_is_rejected():
    client, http = make_client(lambda request: httpx.Response(200, json={"unexpected": 1}))
    try:
        with pytest.raises(RuntimeError, match="message.content"):
            client.generate_structured([], {})
    finally:
        http.close()

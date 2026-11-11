import httpx
import pytest

from calculator_core.provider import OllamaChatClient


def test_ollama_request_uses_tool_schema_and_persistent_adapter():
    def handler(request):
        assert request.url.path == "/api/chat"
        payload = __import__("json").loads(request.read())
        assert payload["model"] == "qwen3:4b"
        assert payload["tools"][0]["function"]["name"] == "calculate"
        return httpx.Response(200, json={"message": {"content": "42"}})

    http = httpx.Client(transport=httpx.MockTransport(handler))
    client = OllamaChatClient(http_client=http)
    try:
        response = client.chat([], [{"type": "function", "function": {"name": "calculate"}}])
        assert response["message"]["content"] == "42"
    finally:
        http.close()


def test_provider_error_is_sanitized():
    http = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(500, text="secret provider body")
        )
    )
    client = OllamaChatClient(http_client=http)
    try:
        with pytest.raises(RuntimeError, match="HTTP 500") as error:
            client.chat([], [])
        assert "secret provider body" not in str(error.value)
    finally:
        http.close()


def test_bad_provider_response_is_rejected():
    http = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"done": True}))
    )
    client = OllamaChatClient(http_client=http)
    try:
        with pytest.raises(RuntimeError, match="invalid chat response"):
            client.chat([], [])
    finally:
        http.close()

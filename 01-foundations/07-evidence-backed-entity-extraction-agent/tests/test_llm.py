import httpx
import pytest

from app.llm import OllamaClient


def make_client(handler):
    http = httpx.Client(transport=httpx.MockTransport(handler))
    return OllamaClient("http://ollama.test", "qwen3:4b", http_client=http), http


def test_sends_json_schema_to_ollama_native_chat():
    def handler(request):
        assert request.url.path == "/api/chat"
        payload = __import__("json").loads(request.read())
        assert payload["model"] == "qwen3:4b"
        assert payload["format"] == {"type": "object"}
        assert payload["stream"] is False
        return httpx.Response(200, json={"message": {"content": '{"entities": []}'}})

    client, http = make_client(handler)
    try:
        assert client.generate_structured([], {"type": "object"}) == '{"entities": []}'
    finally:
        http.close()


def test_provider_http_error_is_sanitized():
    client, http = make_client(
        lambda request: httpx.Response(503, text="private provider traceback")
    )
    try:
        with pytest.raises(RuntimeError, match="HTTP 503") as error:
            client.generate_structured([], {})
        assert "private provider traceback" not in str(error.value)
    finally:
        http.close()


def test_malformed_response_is_rejected():
    client, http = make_client(lambda request: httpx.Response(200, json={"done": True}))
    try:
        with pytest.raises(RuntimeError, match="message.content"):
            client.generate_structured([], {})
    finally:
        http.close()


def test_invalid_configuration_is_rejected():
    with pytest.raises(ValueError, match="model cannot be empty"):
        OllamaClient("http://ollama.test", " ")

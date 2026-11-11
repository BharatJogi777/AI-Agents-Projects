import httpx
import pytest

from app.llm import OllamaClient


def build_client(handler):
    http = httpx.Client(transport=httpx.MockTransport(handler))
    return OllamaClient("http://ollama.test", "qwen3:4b", http_client=http), http


def test_sends_native_ollama_json_schema_request():
    def handler(request):
        assert request.url.path == "/api/chat"
        payload = __import__("json").loads(request.read())
        assert payload["model"] == "qwen3:4b"
        assert payload["stream"] is False
        assert payload["options"]["temperature"] == 0
        assert payload["format"]["type"] == "object"
        return httpx.Response(200, json={"message": {"content": '{"summary":"valid"}'}})

    client, http = build_client(handler)
    try:
        result = client.generate_structured(
            [{"role": "user", "content": "analyze"}],
            {"type": "object"},
        )
        assert result == '{"summary":"valid"}'
    finally:
        http.close()


def test_http_error_is_sanitized():
    client, http = build_client(
        lambda request: httpx.Response(500, text="sensitive provider diagnostics")
    )
    try:
        with pytest.raises(RuntimeError, match="HTTP 500") as error:
            client.generate_structured([], {})
        assert "sensitive provider diagnostics" not in str(error.value)
    finally:
        http.close()


def test_invalid_provider_contract_is_rejected():
    client, http = build_client(lambda request: httpx.Response(200, json={"done": True}))
    try:
        with pytest.raises(RuntimeError, match="message.content"):
            client.generate_structured([], {})
    finally:
        http.close()


def test_invalid_configuration_is_rejected():
    with pytest.raises(ValueError, match="model cannot be empty"):
        OllamaClient("http://ollama.test", " ")

import httpx
import pytest

from app.llm import OllamaChatClient


def make_client(handler, base_url="http://ollama.test/v1"):
    transport = httpx.MockTransport(handler)
    http = httpx.Client(transport=transport)
    return OllamaChatClient(base_url, "qwen3:4b", http_client=http), http


def test_chat_maps_model_messages_and_tool_schemas():
    def handler(request):
        assert request.url.path == "/v1/chat/completions"
        body = request.read().decode()
        assert '"model":"qwen3:4b"' in body
        return httpx.Response(200, json={"choices": [{"message": {"content": "42"}}]})

    client, http = make_client(handler)
    try:
        result = client.chat([{"role": "user", "content": "calculate"}], [])
        assert result["choices"][0]["message"]["content"] == "42"
    finally:
        http.close()


def test_chat_rejects_provider_http_errors_without_leaking_body():
    client, http = make_client(
        lambda request: httpx.Response(500, text="secret provider diagnostic")
    )
    try:
        with pytest.raises(RuntimeError, match="HTTP 500") as error:
            client.chat([], [])
        assert "secret provider diagnostic" not in str(error.value)
    finally:
        http.close()


def test_chat_rejects_invalid_provider_contract():
    client, http = make_client(lambda request: httpx.Response(200, json={"unexpected": True}))
    try:
        with pytest.raises(RuntimeError, match="did not contain choices"):
            client.chat([], [])
    finally:
        http.close()


def test_readiness_requires_configured_model():
    def handler(request):
        assert request.url.path == "/api/tags"
        return httpx.Response(200, json={"models": [{"name": "qwen3:4b"}]})

    client, http = make_client(handler)
    try:
        assert client.is_ready() is True
    finally:
        http.close()


def test_readiness_fails_when_model_is_missing():
    client, http = make_client(
        lambda request: httpx.Response(200, json={"models": [{"name": "llama3.2:3b"}]})
    )
    try:
        assert client.is_ready() is False
    finally:
        http.close()


def test_invalid_client_configuration_is_rejected():
    with pytest.raises(ValueError, match="model cannot be empty"):
        OllamaChatClient("http://ollama.test/v1", " ")

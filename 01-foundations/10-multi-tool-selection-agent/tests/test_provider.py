import httpx
import pytest

from multi_tool_agent.provider import OllamaClient


def test_provider_sends_tool_schemas():
    def handler(request):
        payload = __import__("json").loads(request.read())
        assert request.url.path == "/api/chat"
        assert payload["model"] == "qwen3:4b"
        assert payload["tools"][0]["function"]["name"] == "add_numbers"
        return httpx.Response(200, json={"message": {"content": "done"}})

    http = httpx.Client(transport=httpx.MockTransport(handler))
    client = OllamaClient(http_client=http)
    try:
        assert client.chat([], [{"type": "function", "function": {"name": "add_numbers"}}])["message"]["content"] == "done"
    finally:
        http.close()


def test_provider_http_errors_are_sanitized():
    http = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(502, text="internal upstream details")
        )
    )
    client = OllamaClient(http_client=http)
    try:
        with pytest.raises(RuntimeError, match="HTTP 502") as error:
            client.chat([], [])
        assert "internal upstream details" not in str(error.value)
    finally:
        http.close()


def test_invalid_provider_contract_is_rejected():
    http = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"unexpected": 1}))
    )
    client = OllamaClient(http_client=http)
    try:
        with pytest.raises(RuntimeError, match="invalid chat response"):
            client.chat([], [])
    finally:
        http.close()

import pytest

from app.config import ClientConfig


@pytest.mark.parametrize("url", [
    "http://localhost:8000/mcp",
    "http://127.0.0.1:8000/mcp",
    "https://mcp.example.com/mcp",
])
def test_accepts_valid_endpoints(monkeypatch, url):
    monkeypatch.setenv("MCP_SERVER_URL", url)
    assert ClientConfig.from_env().server_url == url


@pytest.mark.parametrize("url", [
    "",
    "file:///tmp/server",
    "http://mcp.example.com/mcp",
    "http://user:password@localhost:8000/mcp",
])
def test_rejects_unsafe_or_invalid_endpoints(monkeypatch, url):
    monkeypatch.setenv("MCP_SERVER_URL", url)
    with pytest.raises(ValueError):
        ClientConfig.from_env()


def test_reads_optional_bearer_token(monkeypatch):
    monkeypatch.setenv("MCP_SERVER_URL", "https://mcp.example.com/mcp")
    monkeypatch.setenv("MCP_BEARER_TOKEN", "secret")
    assert ClientConfig.from_env().bearer_token == "secret"

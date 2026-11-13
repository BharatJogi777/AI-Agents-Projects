import asyncio
import pytest
from app.inventory import ObservabilityClient


def test_rejects_plain_http_remote():
    with pytest.raises(ValueError):
        ObservabilityClient("http://metrics.example.com")


def test_allows_local_http():
    client = ObservabilityClient("http://localhost:9090")
    assert client.base_url == "http://localhost:9090"


def test_rejects_arbitrary_path():
    client = ObservabilityClient("http://localhost:9090")
    with pytest.raises(ValueError):
        asyncio.run(client.query("/admin", {}))

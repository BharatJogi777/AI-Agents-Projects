import pytest
from app.grafana import GrafanaClient


def test_rejects_remote_http():
    with pytest.raises(ValueError):
        GrafanaClient("http://grafana.example", "token")


def test_requires_token():
    with pytest.raises(ValueError):
        GrafanaClient("http://localhost:3000", "")


def test_validates_limit():
    import asyncio
    client = GrafanaClient("http://localhost:3000", "token")
    with pytest.raises(ValueError):
        asyncio.run(client.search_dashboards("", 0))

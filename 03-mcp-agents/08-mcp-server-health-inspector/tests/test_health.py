import asyncio
from types import SimpleNamespace

import pytest

from app.health import inspect_session


class FakeSession:
    _server_info = SimpleNamespace(name="orders")

    async def ping(self):
        return None


class BrokenSession:
    _server_info = None

    async def ping(self):
        raise ConnectionError("private endpoint detail")


class SlowSession:
    _server_info = None

    async def ping(self):
        await asyncio.sleep(1)


@pytest.mark.asyncio
async def test_healthy_session_reports_server_identity():
    report = await inspect_session(FakeSession())
    assert report.status == "healthy"
    assert report.server_name == "orders"
    assert report.error_category is None


@pytest.mark.asyncio
async def test_protocol_error_is_sanitized():
    report = await inspect_session(BrokenSession())
    assert report.status == "unhealthy"
    assert report.error_category == "protocol_or_connection_error"
    assert "private" not in str(report.to_dict())


@pytest.mark.asyncio
async def test_timeout_is_reported():
    report = await inspect_session(SlowSession(), timeout_seconds=0.001)
    assert report.status == "unhealthy"
    assert report.error_category == "timeout"


@pytest.mark.asyncio
async def test_rejects_non_positive_timeout():
    with pytest.raises(ValueError):
        await inspect_session(FakeSession(), timeout_seconds=0)

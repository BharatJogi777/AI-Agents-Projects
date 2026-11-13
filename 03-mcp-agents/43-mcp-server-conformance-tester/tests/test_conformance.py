from types import SimpleNamespace as NS
import pytest
from app.conformance import inspect_session


class Session:
    async def ping(self):
        return None

    async def list_tools(self):
        return NS(tools=[NS(name="lookup", inputSchema={"type": "object"})])


@pytest.mark.asyncio
async def test_healthy_session():
    result = await inspect_session(Session())
    assert result["conformant_for_smoke_checks"] is True
    assert result["tool_count"] == 1


@pytest.mark.asyncio
async def test_ping_failure_stops_checks():
    class Broken(Session):
        async def ping(self):
            raise TimeoutError()
    result = await inspect_session(Broken())
    assert result["ping"] is False
    assert result["tools_listed"] is False
    assert "TimeoutError" in result["errors"][0]


@pytest.mark.asyncio
async def test_duplicate_tools_reported():
    class Duplicate(Session):
        async def list_tools(self):
            tool = NS(name="same", inputSchema={"type": "object"})
            return NS(tools=[tool, tool])
    result = await inspect_session(Duplicate())
    assert any("duplicate" in e for e in result["errors"])

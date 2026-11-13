import asyncio

import pytest

from app.services.invoker import ToolCallTimedOut, ToolInvoker, ToolNotAllowed


class FakeSession:
    def __init__(self, result=None, delay=0):
        self.result = result
        self.delay = delay
        self.calls = []

    async def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        await asyncio.sleep(self.delay)
        return self.result


@pytest.mark.asyncio
async def test_invokes_allowed_tool_and_audits_without_arguments():
    session = FakeSession({"content": "ok"})
    events = []
    invoker = ToolInvoker(session, {"lookup"}, audit=events.append)
    result = await invoker.invoke("lookup", {"secret": "not-logged"}, correlation_id="req-1")
    assert result == {"content": "ok"}
    assert session.calls == [("lookup", {"secret": "not-logged"})]
    assert events[0].outcome == "success"
    assert events[0].correlation_id == "req-1"
    assert not hasattr(events[0], "arguments")


@pytest.mark.asyncio
async def test_denies_unknown_tool_before_network_call():
    session = FakeSession()
    invoker = ToolInvoker(session, {"lookup"})
    with pytest.raises(ToolNotAllowed):
        await invoker.invoke("delete", {})
    assert session.calls == []


@pytest.mark.asyncio
async def test_rejects_non_object_arguments():
    invoker = ToolInvoker(FakeSession(), {"lookup"})
    with pytest.raises(TypeError):
        await invoker.invoke("lookup", ["not", "an", "object"])


@pytest.mark.asyncio
async def test_timeout_is_typed_and_audited():
    events = []
    invoker = ToolInvoker(FakeSession(delay=0.05), {"slow"}, timeout_seconds=0.001, audit=events.append)
    with pytest.raises(ToolCallTimedOut):
        await invoker.invoke("slow", {})
    assert events[0].outcome == "timeout"


def test_configuration_validation():
    with pytest.raises(ValueError):
        ToolInvoker(FakeSession(), set())
    with pytest.raises(ValueError):
        ToolInvoker(FakeSession(), {"lookup"}, timeout_seconds=0)

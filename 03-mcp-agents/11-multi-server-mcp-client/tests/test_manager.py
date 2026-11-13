from types import SimpleNamespace

import pytest

from app.manager import MultiServerClient, MultiServerError


class FakeSession:
    def __init__(self, names):
        self.names = names
        self.calls = []

    async def list_tools(self):
        return SimpleNamespace(tools=[
            SimpleNamespace(name=name, description=f"{name} description") for name in self.names
        ])

    async def call_tool(self, name, arguments):
        self.calls.append((name, arguments))
        return {"tool": name, "arguments": arguments}


@pytest.mark.asyncio
async def test_discovers_and_routes_across_servers():
    orders, inventory = FakeSession(["lookup", "delete"]), FakeSession(["lookup", "reserve"])
    manager = MultiServerClient()
    manager.add_server("orders", orders, allowed_tools={"lookup"})
    manager.add_server("inventory", inventory, allowed_tools={"lookup", "reserve"})
    tools = await manager.discover()
    assert [item["qualified_name"] for item in tools] == [
        "inventory.lookup", "inventory.reserve", "orders.lookup"
    ]
    result = await manager.call("orders.lookup", {"id": "ORD-1"})
    assert result["tool"] == "lookup"
    assert orders.calls == [("lookup", {"id": "ORD-1"})]
    assert inventory.calls == []


@pytest.mark.asyncio
async def test_disallowed_tool_is_never_called():
    session = FakeSession(["lookup"])
    manager = MultiServerClient()
    manager.add_server("orders", session, allowed_tools={"lookup"})
    with pytest.raises(MultiServerError):
        await manager.call("orders.delete", {})
    assert session.calls == []


def test_duplicate_namespace_is_rejected():
    manager = MultiServerClient()
    manager.add_server("orders", FakeSession([]), allowed_tools={"lookup"})
    with pytest.raises(MultiServerError):
        manager.add_server("orders", FakeSession([]), allowed_tools={"lookup"})


def test_invalid_configuration_is_rejected():
    with pytest.raises(ValueError):
        MultiServerClient().add_server("Orders", FakeSession([]), allowed_tools={"lookup"})
    with pytest.raises(ValueError):
        MultiServerClient().add_server("orders", FakeSession([]), allowed_tools=set())


@pytest.mark.asyncio
async def test_arguments_must_be_object():
    manager = MultiServerClient()
    manager.add_server("orders", FakeSession([]), allowed_tools={"lookup"})
    with pytest.raises(TypeError):
        await manager.call("orders.lookup", [])

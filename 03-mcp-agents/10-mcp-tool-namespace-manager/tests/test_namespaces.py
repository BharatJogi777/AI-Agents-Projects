import pytest

from app.namespaces import NamespaceError, NamespaceRegistry


def test_same_tool_name_can_exist_in_separate_servers():
    registry = NamespaceRegistry()
    registry.register("orders", ["lookup"])
    registry.register("inventory", ["lookup"])
    assert registry.resolve("orders.lookup") == ("orders", "lookup")
    assert registry.resolve("inventory.lookup") == ("inventory", "lookup")


def test_duplicate_namespace_is_rejected():
    registry = NamespaceRegistry()
    registry.register("orders", ["lookup"])
    with pytest.raises(NamespaceError, match="already"):
        registry.register("orders", ["cancel"])


def test_unknown_tool_and_malformed_name_are_rejected():
    registry = NamespaceRegistry()
    registry.register("orders", ["lookup"])
    with pytest.raises(NamespaceError):
        registry.resolve("orders.delete")
    with pytest.raises(NamespaceError):
        registry.resolve("orders.lookup.extra")


def test_invalid_tool_names_are_rejected():
    with pytest.raises(NamespaceError):
        NamespaceRegistry().register("orders", ["Delete-All"])


def test_list_is_stable_and_sorted():
    registry = NamespaceRegistry()
    registry.register("orders", ["cancel", "lookup"])
    assert registry.list_tools() == ["orders.cancel", "orders.lookup"]

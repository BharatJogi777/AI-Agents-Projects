import pytest

from app.registry import ToolRecord, ToolRegistry


def record(server="alpha", name="lookup"):
    return ToolRecord(server, name, "Lookup data", "1.0.0",
                      {"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]})


def test_register_filter_and_export():
    registry = ToolRegistry()
    registry.register(record())
    registry.register(record("beta", "search"))
    assert [item.name for item in registry.find(server="alpha")] == ["lookup"]
    assert len(registry.export()) == 2


def test_duplicate_identity_rejected():
    registry = ToolRegistry()
    registry.register(record())
    with pytest.raises(ValueError):
        registry.register(record())


def test_invalid_required_schema_rejected():
    invalid = ToolRecord("a", "b", "", "1", {"type": "object", "properties": {}, "required": ["missing"]})
    with pytest.raises(ValueError):
        ToolRegistry().register(invalid)

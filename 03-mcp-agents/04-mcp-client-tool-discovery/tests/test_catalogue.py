import pytest

from app.services.catalogue import CatalogueError, DiscoveredTool, ToolCatalogue


def tool(name="lookup_order", description="Read an order.", schema=None):
    return DiscoveredTool(name, description, schema or {"type": "object"})


def test_only_allowlisted_tools_are_exposed():
    catalogue = ToolCatalogue({"lookup_order"})
    catalogue.replace([tool(), tool("delete_order")])
    assert [item.name for item in catalogue.public_tools()] == ["lookup_order"]


def test_replace_is_atomic_when_metadata_is_invalid():
    catalogue = ToolCatalogue({"lookup_order"})
    catalogue.replace([tool()])
    with pytest.raises(CatalogueError):
        catalogue.replace([tool(), tool("bad/name")])
    assert [item.name for item in catalogue.public_tools()] == ["lookup_order"]


def test_duplicate_names_are_rejected():
    catalogue = ToolCatalogue({"lookup_order"})
    with pytest.raises(CatalogueError, match="duplicate"):
        catalogue.replace([tool(), tool()])


def test_non_object_schema_is_rejected():
    catalogue = ToolCatalogue({"lookup_order"})
    with pytest.raises(CatalogueError, match="object"):
        catalogue.replace([tool(schema={"type": "array"})])


def test_unlisted_tool_cannot_be_retrieved():
    catalogue = ToolCatalogue({"lookup_order"})
    catalogue.replace([tool()])
    with pytest.raises(CatalogueError, match="not discovered"):
        catalogue.get("delete_order")


def test_empty_allowlist_is_rejected():
    with pytest.raises(ValueError, match="allowed_names"):
        ToolCatalogue(set())

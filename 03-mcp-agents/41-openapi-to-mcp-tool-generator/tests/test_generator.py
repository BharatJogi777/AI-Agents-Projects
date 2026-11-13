import pytest
from app.generator import generate_tool_specs

def test_get_only():
    doc = {"paths": {"/users": {"get": {"operationId": "listUsers"}, "post": {"operationId": "createUser"}}}}
    assert [x["name"] for x in generate_tool_specs(doc)] == ["listUsers"]

def test_duplicate_ids():
    doc = {"paths": {"/a": {"get": {"operationId": "listA"}}, "/b": {"get": {"operationId": "listA"}}}}
    with pytest.raises(ValueError):
        generate_tool_specs(doc)

def test_requires_paths():
    with pytest.raises(ValueError):
        generate_tool_specs({})

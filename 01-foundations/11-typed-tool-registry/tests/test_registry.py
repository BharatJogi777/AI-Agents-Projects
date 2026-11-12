import pytest
from pydantic import BaseModel, ConfigDict

from tool_registry import (
    RegistryLimits,
    ToolExecutionError,
    ToolRegistrationError,
    ToolRegistry,
)


class Args(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    left: int
    right: int


def registry(**kwargs):
    result = ToolRegistry(**kwargs)
    result.register("multiply", "Multiply integers.", Args, lambda a: {"product": a.left * a.right})
    return result


def test_schema_and_execution_return_json_compatible_copy():
    result = registry()
    schema = result.provider_schemas()
    assert result.names() == ("multiply",)
    assert schema[0]["function"]["name"] == "multiply"
    schema[0]["function"]["description"] = "tampered"
    assert result.provider_schemas()[0]["function"]["description"] == "Multiply integers."
    assert result.execute("multiply", {"left": 6, "right": 7}) == {"product": 42}


def test_duplicate_and_unknown_names():
    result = registry()
    with pytest.raises(ToolRegistrationError, match="duplicate"):
        result.register("multiply", "again", Args, lambda a: a)
    with pytest.raises(ToolExecutionError, match="allowlisted"):
        result.execute("delete_all", {})


@pytest.mark.parametrize("name", ["", "Upper", "two-words", "9tool", "a" * 65, "tool.name"])
def test_invalid_tool_names(name):
    with pytest.raises(ToolRegistrationError):
        ToolRegistry().register(name, "Valid description", Args, lambda a: a)


def test_rejects_extra_and_wrongly_typed_arguments():
    with pytest.raises(ToolExecutionError, match="invalid arguments"):
        registry().execute("multiply", {"left": 1, "right": 2, "shell": "id"})
    with pytest.raises(ToolExecutionError, match="invalid arguments"):
        registry().execute("multiply", {"left": "1", "right": 2})


@pytest.mark.parametrize("arguments", [None, [], "{}", 12])
def test_arguments_must_be_object(arguments):
    with pytest.raises(ToolExecutionError, match="JSON object"):
        registry().execute("multiply", arguments)


def test_handler_failure_is_wrapped_without_leaking_message():
    result = ToolRegistry()
    result.register("explode", "Raise.", Args, lambda _: (_ for _ in ()).throw(RuntimeError("secret")))
    with pytest.raises(ToolExecutionError, match="handler failed") as err:
        result.execute("explode", {"left": 1, "right": 2})
    assert "secret" not in str(err.value)
    assert isinstance(err.value.__cause__, RuntimeError)


def test_freeze_prevents_runtime_registration():
    result = registry()
    result.freeze()
    result.freeze()
    assert result.is_frozen
    with pytest.raises(ToolRegistrationError, match="frozen"):
        result.register("subtract", "Subtract.", Args, lambda a: a)


def test_tool_count_limit():
    result = ToolRegistry(RegistryLimits(max_tools=1))
    result.register("first", "First.", Args, lambda a: a)
    with pytest.raises(ToolRegistrationError, match="maximum"):
        result.register("second", "Second.", Args, lambda a: a)


def test_description_limit():
    result = ToolRegistry(RegistryLimits(max_description_chars=5))
    with pytest.raises(ToolRegistrationError, match="description"):
        result.register("first", "too long", Args, lambda a: a)


def test_result_must_be_json_serializable():
    result = ToolRegistry()
    result.register("bad_result", "Returns an unsupported object.", Args, lambda _: object())
    with pytest.raises(ToolExecutionError, match="non-JSON"):
        result.execute("bad_result", {"left": 1, "right": 2})


def test_result_rejects_nan():
    result = ToolRegistry()
    result.register("bad_number", "Returns NaN.", Args, lambda _: float("nan"))
    with pytest.raises(ToolExecutionError, match="non-JSON"):
        result.execute("bad_number", {"left": 1, "right": 2})


def test_result_byte_limit():
    result = ToolRegistry(RegistryLimits(max_result_bytes=8))
    result.register("large", "Returns a large string.", Args, lambda _: {"value": "x" * 20})
    with pytest.raises(ToolExecutionError, match="byte limit"):
        result.execute("large", {"left": 1, "right": 2})


def test_invalid_limits_rejected():
    with pytest.raises(ValueError):
        RegistryLimits(max_tools=True)
    with pytest.raises(ValueError):
        RegistryLimits(max_result_bytes=0)

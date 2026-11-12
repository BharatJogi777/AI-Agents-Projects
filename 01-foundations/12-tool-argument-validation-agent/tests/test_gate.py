import json

import pytest
from pydantic import BaseModel, ConfigDict

from app import ArgumentGate, SearchArgs, ToolCallRejected, build_demo_gate
from tool_gate import GateLimits, ToolHandlerFailed


@pytest.mark.parametrize(
    "payload",
    [
        '{"query":"agents","limit":5}',
        '{"query":"agents","limit":5,"extra":true}',
        '{"query":"agents","limit":"5"}',
        '{bad json',
        '[]',
        'null',
        '{"query":"x","limit":NaN}',
        '{"query":"first","query":"second","limit":2}',
    ],
)
def test_json_validation_gate(payload):
    gate = build_demo_gate()
    if payload == '{"query":"agents","limit":5}':
        assert gate.validate_and_execute("search", payload)["ok"] is True
    else:
        with pytest.raises(ToolCallRejected):
            gate.validate_and_execute("search", payload)


def test_unknown_tool_rejected_before_argument_parsing():
    with pytest.raises(ToolCallRejected, match="allowlisted"):
        build_demo_gate().validate_and_execute("shell", "{not json")


def test_handler_failure_is_distinct_from_schema_error():
    gate = ArgumentGate({"search": SearchArgs}, {"search": lambda _: 1 / 0})
    with pytest.raises(ToolHandlerFailed, match="trusted handler failed") as err:
        gate.validate_and_execute("search", {"query": "x", "limit": 2})
    assert isinstance(err.value.__cause__, ZeroDivisionError)


def test_registry_schema_handler_mismatch_rejected():
    with pytest.raises(ValueError, match="exactly one handler"):
        ArgumentGate({"search": SearchArgs}, {})


def test_non_string_or_unknown_tool_name_rejected():
    gate = build_demo_gate()
    for name in (None, [], {}, 1):
        with pytest.raises(ToolCallRejected, match="allowlisted"):
            gate.validate(name, {})


def test_arguments_must_be_json_object():
    gate = build_demo_gate()
    for raw in ([], None, "5", '"text"', "null"):
        with pytest.raises(ToolCallRejected, match="JSON object"):
            gate.validate("search", raw)


def test_argument_byte_limit_applies_before_json_parse():
    gate = ArgumentGate(
        {"search": SearchArgs},
        {"search": lambda args: {}},
        max_argument_bytes=128,
    )
    with pytest.raises(ToolCallRejected, match="size limit"):
        gate.validate("search", '{"query":"' + "x" * 200 + '","limit":1}')


def test_validation_feedback_does_not_echo_input_values():
    secret = "do-not-echo-this"
    gate = build_demo_gate()
    with pytest.raises(ToolCallRejected) as err:
        gate.validate("search", {"query": secret, "limit": "not-an-int"})
    assert secret not in str(err.value)
    feedback = json.loads(str(err.value))
    assert feedback["validation_errors"]


def test_input_dict_must_be_json_serializable():
    gate = build_demo_gate()
    with pytest.raises(ToolCallRejected, match="JSON values"):
        gate.validate("search", {"query": "x", "limit": 1, "bad": object()})


def test_handler_output_is_detached_and_bounded():
    class Args(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        query: str
    shared = {"items": [1, 2]}
    gate = ArgumentGate({"search": Args}, {"search": lambda _: shared})
    response = gate.execute("search", {"query": "x"})
    response["result"]["items"].append(3)
    assert shared == {"items": [1, 2]}

    small = ArgumentGate(
        {"search": Args},
        {"search": lambda _: {"value": "x" * 200}},
        max_result_bytes=128,
    )
    with pytest.raises(ToolHandlerFailed, match="size limit"):
        small.execute("search", {"query": "x"})


def test_handler_output_must_be_json_safe():
    class Args(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        query: str
    gate = ArgumentGate({"search": Args}, {"search": lambda _: float("nan")})
    with pytest.raises(ToolHandlerFailed, match="non-JSON"):
        gate.execute("search", {"query": "x"})


def test_limits_validate_and_are_immutable():
    with pytest.raises(ValueError):
        GateLimits(max_argument_bytes=10)
    limits = GateLimits(max_argument_bytes=256, max_result_bytes=512)
    gate = ArgumentGate({"search": SearchArgs}, {"search": lambda _: {}}, limits=limits)
    assert gate.validate("search", {"query": "x", "limit": 1}).limit == 1


def test_schema_and_handler_mappings_are_copied():
    schemas = {"search": SearchArgs}
    handlers = {"search": lambda _: {"items": []}}
    gate = ArgumentGate(schemas, handlers)
    schemas.clear()
    handlers.clear()
    assert gate.execute("search", {"query": "x", "limit": 1})["ok"]

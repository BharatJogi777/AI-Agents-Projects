import pytest
from app import ArgumentGate,SearchArgs,ToolCallRejected,build_demo_gate

@pytest.mark.parametrize("payload",[
    '{"query":"agents","limit":5}', '{"query":"agents","limit":5,"extra":true}',
    '{"query":"agents","limit":"5"}', '{bad json', '[]', 'null'
])
def test_validation_gate(payload):
    gate=build_demo_gate()
    if payload=='{"query":"agents","limit":5}':
        assert gate.validate_and_execute("search",payload)["ok"] is True
    else:
        with pytest.raises(ToolCallRejected): gate.validate_and_execute("search",payload)

def test_unknown_tool_rejected():
    with pytest.raises(ToolCallRejected,match="allowlisted"):
        build_demo_gate().validate_and_execute("shell",{})

def test_handler_failure_is_distinct_from_schema_error():
    gate=ArgumentGate({"search":SearchArgs},{"search":lambda _:1/0})
    with pytest.raises(RuntimeError,match="trusted handler failed"):
        gate.validate_and_execute("search",{"query":"x","limit":2})

def test_registry_schema_handler_mismatch_rejected():
    with pytest.raises(ValueError,match="exactly one handler"):
        ArgumentGate({"search":SearchArgs},{})

import json
import pytest

from app.agent import AgentProtocolError, AgentStepLimitError, ToolCallingAgent
from app.tools import execute_tool


class FakeClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def chat(self, messages, tools):
        self.calls.append((messages, tools))
        return next(self.responses)


def tool_response(name="add_numbers", arguments='{"a": 19, "b": 23}', call_id="call-1"):
    return {"choices": [{"message": {
        "role": "assistant", "content": None,
        "tool_calls": [{"id": call_id, "type": "function",
                        "function": {"name": name, "arguments": arguments}}],
    }}]}


def test_agent_executes_allowlisted_tool_then_returns_final_answer():
    client = FakeClient([
        tool_response(),
        {"choices": [{"message": {"role": "assistant", "content": "The answer is 42."}}]},
    ])
    result = ToolCallingAgent(client, max_steps=3).run("What is 19 + 23?")
    assert result == "The answer is 42."
    tool_message = next(m for m in client.calls[1][0] if m["role"] == "tool")
    assert json.loads(tool_message["content"]) == {"ok": True, "result": {"result": 42.0}}


def test_unknown_tool_is_not_executed_and_error_is_returned_to_model():
    client = FakeClient([
        tool_response(name="run_shell", arguments="{}"),
        {"choices": [{"message": {"role": "assistant", "content": "I cannot run shell commands."}}]},
    ])
    assert ToolCallingAgent(client).run("Run a shell command") == "I cannot run shell commands."
    tool_message = next(m for m in client.calls[1][0] if m["role"] == "tool")
    assert '"ok": false' in tool_message["content"]
    assert "allowlisted" not in tool_message["content"]


def test_step_limit_is_enforced():
    agent = ToolCallingAgent(FakeClient([tool_response()]), max_steps=1)
    with pytest.raises(AgentStepLimitError):
        agent.run("Add 1 and 2")


def test_empty_input_is_rejected():
    with pytest.raises(ValueError, match="cannot be empty"):
        ToolCallingAgent(FakeClient([])).run("   ")


def test_tool_arguments_are_validated():
    with pytest.raises(ValueError, match="Invalid arguments"):
        execute_tool("add_numbers", {"a": "not-a-number"})


def test_tool_argument_size_is_bounded():
    client = FakeClient([
        tool_response(arguments='{"a":"' + ("x" * 5000) + '"}'),
        {"choices": [{"message": {"role": "assistant", "content": "Rejected safely."}}]},
    ])
    assert ToolCallingAgent(client).run("Try an oversized tool call") == "Rejected safely."


def test_too_many_tool_calls_are_rejected_before_any_tool_runs():
    response = {"choices": [{"message": {
        "role": "assistant", "content": None,
        "tool_calls": [
            {"id": f"call-{i}", "type": "function",
             "function": {"name": "add_numbers", "arguments": '{"a":1,"b":2}'}}
            for i in range(5)
        ],
    }}]}
    with pytest.raises(AgentProtocolError, match="tool-call limit"):
        ToolCallingAgent(FakeClient([response]), max_tool_calls_per_step=4).run("Add values")

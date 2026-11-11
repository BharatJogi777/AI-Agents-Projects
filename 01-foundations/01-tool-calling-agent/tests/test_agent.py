import json

import pytest

from app.agent import AgentStepLimitError, ToolCallingAgent
from app.tools import execute_tool


class FakeClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def chat(self, messages, tools):
        self.calls.append((messages, tools))
        return next(self.responses)


def test_agent_executes_allowlisted_tool_then_returns_final_answer():
    client = FakeClient([
        {"choices": [{"message": {
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": "call-1",
                "type": "function",
                "function": {"name": "add_numbers", "arguments": '{"a": 19, "b": 23}'},
            }],
        }}]},
        {"choices": [{"message": {"role": "assistant", "content": "The answer is 42."}}]},
    ])

    result = ToolCallingAgent(client, max_steps=3).run("What is 19 + 23?")
    assert result == "The answer is 42."
    second_messages = client.calls[1][0]
    tool_message = next(message for message in second_messages if message["role"] == "tool")
    assert json.loads(tool_message["content"]) == {"ok": True, "result": {"result": 42.0}}


def test_unknown_tool_is_not_executed_and_error_is_returned_to_model():
    client = FakeClient([
        {"choices": [{"message": {
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": "call-unknown",
                "type": "function",
                "function": {"name": "run_shell", "arguments": "{}"},
            }],
        }}]},
        {"choices": [{"message": {"role": "assistant", "content": "I cannot run shell commands."}}]},
    ])

    assert ToolCallingAgent(client).run("Run a shell command") == "I cannot run shell commands."
    tool_message = next(message for message in client.calls[1][0] if message["role"] == "tool")
    assert '"ok": false' in tool_message["content"]


def test_step_limit_is_enforced():
    response = {"choices": [{"message": {
        "role": "assistant",
        "content": None,
        "tool_calls": [{
            "id": "call-1",
            "type": "function",
            "function": {"name": "add_numbers", "arguments": '{"a": 1, "b": 2}'},
        }],
    }}]}
    agent = ToolCallingAgent(FakeClient([response]), max_steps=1)

    with pytest.raises(AgentStepLimitError):
        agent.run("Add 1 and 2")


def test_empty_input_is_rejected():
    with pytest.raises(ValueError, match="cannot be empty"):
        ToolCallingAgent(FakeClient([])).run("   ")


def test_tool_arguments_are_validated():
    with pytest.raises(ValueError, match="Invalid arguments"):
        execute_tool("add_numbers", {"a": "not-a-number"})

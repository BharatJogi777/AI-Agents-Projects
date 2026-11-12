import pytest

from multi_tool_agent import MultiToolAgent
from multi_tool_agent.agent import AgentError


class Fake:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def chat(self, messages, tools):
        self.calls.append((messages, tools))
        return next(self.responses)


def call(name, args, call_id=None):
    item = {"function": {"name": name, "arguments": args}}
    if call_id is not None:
        item["id"] = call_id
    return {"message": {"role": "assistant", "content": "", "tool_calls": [item]}}


def answer(value="Done."):
    return {"message": {"role": "assistant", "content": value}}


def test_tool_selection_execution_and_registry_schemas():
    fake = Fake([call("add_numbers", '{"a":2,"b":3}'), answer("The sum is 5.")])
    assert MultiToolAgent(fake).run("Add 2 and 3") == "The sum is 5."
    assert {t["function"]["name"] for t in fake.calls[0][1]} == {
        "add_numbers", "text_length", "current_time"
    }
    assert '"sum":5.0' in fake.calls[1][0][-1]["content"]


def test_multiple_tools_in_one_model_turn_are_executed():
    multi = {"message": {"role": "assistant", "content": "", "tool_calls": [
        {"id": "c1", "function": {"name": "add_numbers", "arguments": {"a": 2, "b": 4}}},
        {"id": "c2", "function": {"name": "text_length", "arguments": {"text": "hello"}}},
    ]}}
    fake = Fake([multi, answer("Both tools completed.")])
    assert MultiToolAgent(fake).run("Add 2 and 4 and count hello") == "Both tools completed."
    messages = fake.calls[1][0]
    assert messages[-2]["tool_call_id"] == "c1"
    assert messages[-1]["tool_call_id"] == "c2"
    assert '"sum":6.0' in messages[-2]["content"]
    assert '"length":5' in messages[-1]["content"]


def test_unknown_tool_and_invalid_arguments_fail_closed_without_echoing_values():
    fake = Fake([
        call("shell", '{"command":"secret-command"}'),
        answer("Not available."),
    ])
    MultiToolAgent(fake).run("run shell")
    result = fake.calls[1][0][-1]["content"]
    assert '"ok":false' in result
    assert "secret-command" not in result

    fake = Fake([
        call("add_numbers", '{"a":2,"b":3,"command":"id"}'),
        answer("Bad arguments."),
    ])
    MultiToolAgent(fake).run("add")
    assert "Invalid or unsupported" in fake.calls[1][0][-1]["content"]


def test_non_finite_numbers_are_rejected():
    fake = Fake([call("add_numbers", '{"a":NaN,"b":3}'), answer("Bad arguments.")])
    MultiToolAgent(fake).run("add")
    assert '"ok":false' in fake.calls[1][0][-1]["content"]


def test_timezone_tool_and_invalid_timezone():
    fake = Fake([
        call("current_time", '{"timezone":"Asia/Kolkata"}'),
        answer("It is now in India."),
    ])
    assert "India" in MultiToolAgent(fake).run("what time is it in India?")
    assert '"timezone":"Asia/Kolkata"' in fake.calls[1][0][-1]["content"]

    fake = Fake([call("current_time", '{"timezone":"Mars/Olympus"}'), answer("Invalid zone.")])
    MultiToolAgent(fake).run("time on Mars")
    assert '"ok":false' in fake.calls[1][0][-1]["content"]


def test_duplicate_call_ids_are_rejected():
    response = {"message": {"role": "assistant", "content": "", "tool_calls": [
        {"id": "same", "function": {"name": "add_numbers", "arguments": {"a": 1, "b": 2}}},
        {"id": "same", "function": {"name": "text_length", "arguments": {"text": "x"}}},
    ]}}
    with pytest.raises(AgentError, match="duplicate"):
        MultiToolAgent(Fake([response])).run("do both")


def test_call_limit_and_agent_step_limit():
    many = {"message": {"role": "assistant", "content": "", "tool_calls": [
        {"function": {"name": "text_length", "arguments": {"text": "x"}}}
        for _ in range(3)
    ]}}
    with pytest.raises(AgentError, match="per-step"):
        MultiToolAgent(Fake([many]), max_tool_calls_per_step=2).run("count")

    with pytest.raises(AgentError, match="step limit"):
        MultiToolAgent(Fake([call("add_numbers", '{"a":1,"b":2}')]), max_steps=1).run("add")


def test_prompt_and_final_answer_byte_limits():
    fake = Fake([])
    with pytest.raises(ValueError, match="byte limit"):
        MultiToolAgent(fake).run("x" * 32_001)
    assert fake.calls == []

    with pytest.raises(AgentError, match="Final answer"):
        MultiToolAgent(Fake([answer("é" * 10)]), max_final_bytes=10).run("hello")


def test_empty_prompt_and_configuration_validation():
    with pytest.raises(ValueError):
        MultiToolAgent(Fake([])).run(" ")
    for kwargs in ({"max_steps": 0}, {"max_tool_calls_per_step": 9}, {"max_prompt_bytes": 0}):
        with pytest.raises(ValueError):
            MultiToolAgent(Fake([]), **kwargs)

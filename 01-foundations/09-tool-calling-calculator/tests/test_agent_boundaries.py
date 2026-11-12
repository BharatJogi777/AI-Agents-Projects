import json

import pytest

from calculator_core.agent import CalculatorAgent


class FakeClient:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def chat(self, messages, tools):
        self.calls.append((messages, tools))
        return next(self.responses)


def response_with_calls(calls):
    return {"message": {"role": "assistant", "content": "", "tool_calls": calls}}


def one_call(call_id="calc-1", arguments='{"expression":"6 * 7"}'):
    return {
        "id": call_id,
        "type": "function",
        "function": {"name": "calculate", "arguments": arguments},
    }


def final_response(content="42"):
    return {"message": {"role": "assistant", "content": content}}


def test_tool_result_is_correlated_with_provider_call_id():
    client = FakeClient([
        response_with_calls([one_call("tool-call-abc")]),
        final_response("The answer is 42."),
    ])
    assert CalculatorAgent(client).run("Calculate 6 times 7") == "The answer is 42."
    tool_message = client.calls[1][0][-1]
    assert tool_message["role"] == "tool"
    assert tool_message["tool_call_id"] == "tool-call-abc"
    assert json.loads(tool_message["content"])["result"]["result"] == "42"


def test_too_many_tool_calls_in_one_response_fail_closed():
    calls = [one_call(f"id-{i}") for i in range(4)]
    client = FakeClient([response_with_calls(calls)])
    with pytest.raises(RuntimeError, match="per-step tool-call limit"):
        CalculatorAgent(client, max_tool_calls_per_step=3).run("Do calculations")
    assert len(client.calls) == 1


@pytest.mark.parametrize("bad_calls", ["not-a-list", {}, "string"])
def test_malformed_tool_calls_are_rejected(bad_calls):
    client = FakeClient([{"message": {"role": "assistant", "tool_calls": bad_calls}}])
    with pytest.raises(RuntimeError, match="Malformed tool_calls"):
        CalculatorAgent(client).run("Calculate")


def test_final_answer_byte_limit_is_enforced():
    client = FakeClient([final_response("é" * 100)])
    with pytest.raises(RuntimeError, match="final answer exceeded"):
        CalculatorAgent(client, max_final_answer_bytes=100).run("Explain")


def test_tool_arguments_must_be_json_object():
    call = one_call(arguments='["not", "an", "object"]')
    client = FakeClient([
        response_with_calls([call]),
        final_response("The tool arguments were invalid."),
    ])
    assert "invalid" in CalculatorAgent(client).run("Calculate something")
    tool_result = json.loads(client.calls[1][0][-1]["content"])
    assert tool_result["ok"] is False


def test_request_utf8_byte_limit_is_checked_before_model_call():
    client = FakeClient([])
    with pytest.raises(ValueError, match="32000-byte"):
        CalculatorAgent(client).run("é" * 16_001)
    assert client.calls == []


def test_configuration_limits_are_validated():
    client = FakeClient([])
    with pytest.raises(ValueError, match="max_steps"):
        CalculatorAgent(client, max_steps=6)
    with pytest.raises(ValueError, match="max_tool_calls_per_step"):
        CalculatorAgent(client, max_tool_calls_per_step=6)
    with pytest.raises(ValueError, match="max_final_answer_bytes"):
        CalculatorAgent(client, max_final_answer_bytes=10)

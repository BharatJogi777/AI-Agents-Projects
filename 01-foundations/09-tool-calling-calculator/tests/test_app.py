import json
import pytest
from app import AgentStepLimitError, CalculationError, CalculatorAgent, calculate, execute_tool


@pytest.mark.parametrize(("expression", "expected"), [
    ("1 + 2 * 3", "7"), ("(1 + 2) * 3", "9"), ("10 / 4", "2.5"),
    ("2 ** 3", "8"), ("-5 + +2", "-3"), ("10 // 3", "3"),
    ("10 % 3", "1"), ("0.1 + 0.2", "0.3")
])
def test_calculate(expression, expected):
    assert calculate(expression) == expected


@pytest.mark.parametrize("expression", [
    "", " ", "1 / 0", "2 ** 100", "2 ** 1.5", "__import__('os').system('id')",
    "open('/etc/passwd')", "1 < 2", "x + 1", "[1, 2]", "True + 1"
])
def test_rejects_invalid_expression(expression):
    with pytest.raises(CalculationError):
        calculate(expression)


def test_expression_length_is_bounded():
    with pytest.raises(CalculationError, match="too long"):
        calculate("1+" + "1+" * 130 + "1")


class FakeClient:
    def __init__(self, responses):
        self.responses, self.calls = iter(responses), []

    def chat(self, messages, tools):
        self.calls.append((messages, tools))
        return next(self.responses)


def tool_call(name="calculate", arguments='{"expression":"19 + 23"}'):
    return {"message": {"role": "assistant", "content": "", "tool_calls": [
        {"id": "call-1", "function": {"name": name, "arguments": arguments}}
    ]}}


def test_agent_calls_tool_then_returns_answer():
    client = FakeClient([tool_call(), {"message": {"role": "assistant", "content": "19 + 23 = 42."}}])
    assert CalculatorAgent(client).run("What is 19 + 23?") == "19 + 23 = 42."
    assert json.loads(client.calls[1][0][-1]["content"])["result"]["result"] == "42"


def test_unknown_tool_fails_closed():
    client = FakeClient([tool_call("run_shell", "{}"), {"message": {"role": "assistant", "content": "I cannot run shell."}}])
    assert "cannot run shell" in CalculatorAgent(client).run("Run shell")
    assert json.loads(client.calls[1][0][-1]["content"])["ok"] is False


def test_step_limit_and_argument_validation():
    with pytest.raises(AgentStepLimitError):
        CalculatorAgent(FakeClient([tool_call()]), max_steps=1).run("calculate")
    with pytest.raises(ValueError, match="Invalid calculate arguments"):
        execute_tool("calculate", {"expression": "1+1", "extra": "bad"})


def test_empty_request_rejected():
    with pytest.raises(ValueError, match="cannot be empty"):
        CalculatorAgent(FakeClient([])).run(" ")

import pytest

from app import MultiToolAgent


class Fake:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def chat(self, messages, tools):
        self.calls.append((messages, tools))
        return next(self.responses)


def call(name, args):
    return {"message": {"role": "assistant", "content": "", "tool_calls": [
        {"function": {"name": name, "arguments": args}}
    ]}}


def test_multi_tool_selection_and_execution():
    fake = Fake([
        call("add_numbers", '{"a":2,"b":3}'),
        {"message": {"role": "assistant", "content": "The sum is 5."}},
    ])
    assert MultiToolAgent(fake).run("Add 2 and 3") == "The sum is 5."
    assert len(fake.calls[0][1]) == 3
    assert '"sum": 5.0' in fake.calls[1][0][-1]["content"]


def test_unknown_tool_fails_closed():
    fake = Fake([
        call("shell", "{}"),
        {"message": {"role": "assistant", "content": "Not available."}},
    ])
    MultiToolAgent(fake).run("run shell")
    assert '"ok": false' in fake.calls[1][0][-1]["content"]


def test_extra_fields_and_non_finite_numbers_are_rejected():
    fake = Fake([
        call("add_numbers", '{"a":2,"b":3,"command":"id"}'),
        {"message": {"role": "assistant", "content": "Bad arguments."}},
    ])
    MultiToolAgent(fake).run("add")
    assert '"ok": false' in fake.calls[1][0][-1]["content"]

    fake = Fake([
        call("add_numbers", '{"a":NaN,"b":3}'),
        {"message": {"role": "assistant", "content": "Bad arguments."}},
    ])
    MultiToolAgent(fake).run("add")
    assert '"ok": false' in fake.calls[1][0][-1]["content"]


def test_empty_prompt_and_step_limit():
    with pytest.raises(ValueError):
        MultiToolAgent(Fake([])).run(" ")
    with pytest.raises(RuntimeError, match="exceeded"):
        MultiToolAgent(Fake([call("add_numbers", '{"a":1,"b":2}')]), max_steps=1).run("add")


def test_prompt_size_is_bounded_before_model_call():
    fake = Fake([])
    with pytest.raises(ValueError, match="byte limit"):
        MultiToolAgent(fake).run("x" * 32_001)
    assert fake.calls == []

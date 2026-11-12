import sys
import types
import pytest

from app.budget import BudgetConfig, BudgetPlanner, ContextItem
from app.token_counting import TokenCountError, TiktokenCounter


class BrokenCounter:
    def __init__(self, result):
        self.result = result
    def count(self, text):
        return self.result


@pytest.mark.parametrize("invalid", [-1, 1.5, True, "4", None])
def test_counter_output_must_be_a_non_negative_integer(invalid):
    planner = BudgetPlanner(BrokenCounter(invalid), BudgetConfig(100, 10, 5, 4))
    with pytest.raises(TokenCountError):
        planner.plan([ContextItem("required", "system", "hello", mandatory=True)])


def test_negative_raw_count_is_not_hidden_by_item_overhead():
    planner = BudgetPlanner(BrokenCounter(-2), BudgetConfig(100, 10, 5, 4))
    with pytest.raises(TokenCountError):
        planner.plan([ContextItem("required", "system", "hello", mandatory=True)])


def test_tiktoken_counter_uses_model_encoding(monkeypatch):
    fake_encoding = types.SimpleNamespace(encode=lambda text: list(text.split()))
    fake_module = types.SimpleNamespace(encoding_for_model=lambda model: fake_encoding)
    monkeypatch.setitem(sys.modules, "tiktoken", fake_module)
    counter = TiktokenCounter(model="gpt-4o")
    assert counter.count("one two three") == 3


def test_tiktoken_counter_uses_explicit_encoding(monkeypatch):
    fake_encoding = types.SimpleNamespace(encode=lambda text: [1, 2])
    fake_module = types.SimpleNamespace(get_encoding=lambda name: fake_encoding)
    monkeypatch.setitem(sys.modules, "tiktoken", fake_module)
    counter = TiktokenCounter(encoding_name="cl100k_base")
    assert counter.count("some text") == 2


def test_tiktoken_requires_exactly_one_selector():
    with pytest.raises(ValueError, match="exactly one"):
        TiktokenCounter()
    with pytest.raises(ValueError, match="exactly one"):
        TiktokenCounter(model="gpt-4o", encoding_name="cl100k_base")


def test_budget_configuration_requires_integer_values():
    with pytest.raises(TypeError, match="integers"):
        BudgetConfig(100, 20.5)

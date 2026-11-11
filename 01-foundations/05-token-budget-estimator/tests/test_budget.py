import pytest

from app.budget import (
    BudgetConfig,
    BudgetPlanner,
    ContextItem,
    MandatoryContextOverflow,
)
from app.token_counting import FixedTokenCounter, HeuristicTokenCounter


def make_planner(counts, budget=20):
    return BudgetPlanner(
        FixedTokenCounter(counts),
        BudgetConfig(
            context_window_tokens=budget + 8,
            reserved_output_tokens=5,
            safety_margin_tokens=3,
        ),
    )


def test_output_reserve_and_safety_margin_are_removed_from_input_budget():
    config = BudgetConfig(100, reserved_output_tokens=20, safety_margin_tokens=10)
    assert config.available_input_tokens == 70


def test_mandatory_items_are_kept_before_optional_items():
    planner = make_planner({"system": 8, "user": 7, "history": 10})
    plan = planner.plan([
        ContextItem("history", "history", "history", priority=100),
        ContextItem("system", "system", "system", mandatory=True),
        ContextItem("user", "user", "user", mandatory=True),
    ])
    assert [entry.item.item_id for entry in plan.included] == ["system", "user"]
    assert [entry.item.item_id for entry in plan.dropped] == ["history"]
    assert plan.estimated_input_tokens == 15


def test_optional_items_are_selected_by_priority_and_returned_in_input_order():
    planner = make_planner({"low": 5, "high": 8, "medium": 7, "high-tie": 4})
    plan = planner.plan([
        ContextItem("low", "history", "low", priority=1),
        ContextItem("high", "retrieval", "high", priority=10),
        ContextItem("medium", "tool", "medium", priority=5),
        ContextItem("high-tie", "history", "high-tie", priority=10),
    ])
    assert [entry.item.item_id for entry in plan.included] == ["high", "medium", "high-tie"]
    assert [entry.item.item_id for entry in plan.dropped] == ["low"]


def test_item_that_does_not_fit_is_dropped_without_truncation():
    planner = make_planner({"system": 5, "large": 21})
    plan = planner.plan([
        ContextItem("system", "system", "system", mandatory=True),
        ContextItem("large", "retrieval", "large", priority=99),
    ])
    assert [entry.item.item_id for entry in plan.dropped] == ["large"]


def test_mandatory_overflow_fails_explicitly():
    planner = make_planner({"system": 21})
    with pytest.raises(MandatoryContextOverflow, match="does not fit"):
        planner.plan([ContextItem("system", "system", "system", mandatory=True)])


def test_duplicate_item_ids_are_rejected():
    planner = make_planner({"same": 1})
    with pytest.raises(ValueError, match="unique"):
        planner.plan([
            ContextItem("same", "history", "same"),
            ContextItem("same", "history", "same"),
        ])


def test_invalid_budget_configuration_is_rejected():
    with pytest.raises(ValueError, match="smaller"):
        BudgetConfig(100, reserved_output_tokens=80, safety_margin_tokens=20)


def test_heuristic_counter_is_labelled_and_validated():
    counter = HeuristicTokenCounter(chars_per_token=4)
    assert counter.count("") == 0
    assert counter.count("abcdefgh") == 2
    with pytest.raises(ValueError):
        HeuristicTokenCounter(chars_per_token=0)

"""Deterministic context admission under a finite input-token budget."""
from dataclasses import dataclass
from typing import Sequence

from app.token_counting import TokenCounter, TokenCountError


@dataclass(frozen=True)
class BudgetConfig:
    context_window_tokens: int
    reserved_output_tokens: int
    safety_margin_tokens: int = 0
    per_item_overhead_tokens: int = 0

    def __post_init__(self) -> None:
        values = (self.context_window_tokens, self.reserved_output_tokens,
                  self.safety_margin_tokens, self.per_item_overhead_tokens)
        if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
            raise TypeError("token budget values must be integers")
        if any(value < 0 for value in values):
            raise ValueError("token budget values cannot be negative")
        if self.context_window_tokens == 0:
            raise ValueError("context_window_tokens must be greater than zero")
        if self.reserved_output_tokens + self.safety_margin_tokens >= self.context_window_tokens:
            raise ValueError("output reserve plus safety margin must be smaller than context window")

    @property
    def available_input_tokens(self) -> int:
        return self.context_window_tokens - self.reserved_output_tokens - self.safety_margin_tokens


@dataclass(frozen=True)
class ContextItem:
    item_id: str
    kind: str
    text: str
    priority: int = 0
    mandatory: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise ValueError("item_id cannot be empty")
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("kind cannot be empty")
        if not isinstance(self.text, str):
            raise TypeError("context text must be a string")
        if not isinstance(self.priority, int) or isinstance(self.priority, bool):
            raise TypeError("priority must be an integer")
        if not isinstance(self.mandatory, bool):
            raise TypeError("mandatory must be a boolean")


@dataclass(frozen=True)
class PlannedItem:
    item: ContextItem
    estimated_tokens: int


@dataclass(frozen=True)
class BudgetPlan:
    available_input_tokens: int
    estimated_input_tokens: int
    remaining_input_tokens: int
    included: tuple[PlannedItem, ...]
    dropped: tuple[PlannedItem, ...]


class MandatoryContextOverflow(ValueError):
    """Required context cannot fit without violating the budget."""


class BudgetPlanner:
    def __init__(self, counter: TokenCounter, config: BudgetConfig) -> None:
        self._counter = counter
        self._config = config

    def _measure(self, item: ContextItem) -> PlannedItem:
        raw_count = self._counter.count(item.text)
        if (not isinstance(raw_count, int) or isinstance(raw_count, bool)
                or raw_count < 0):
            raise TokenCountError(
                f"counter returned invalid count for item {item.item_id!r}: {raw_count!r}"
            )
        return PlannedItem(item, raw_count + self._config.per_item_overhead_tokens)

    def plan(self, items: Sequence[ContextItem]) -> BudgetPlan:
        ids = [item.item_id for item in items]
        if len(ids) != len(set(ids)):
            raise ValueError("context item IDs must be unique")

        measured = [self._measure(item) for item in items]
        budget = self._config.available_input_tokens
        included_ids: set[str] = set()
        used = 0

        mandatory = [entry for entry in measured if entry.item.mandatory]
        optional = [entry for entry in measured if not entry.item.mandatory]

        for entry in mandatory:
            if used + entry.estimated_tokens > budget:
                raise MandatoryContextOverflow(
                    f"mandatory item {entry.item.item_id!r} does not fit: "
                    f"{used + entry.estimated_tokens} > {budget} input tokens"
                )
            included_ids.add(entry.item.item_id)
            used += entry.estimated_tokens

        # Python's sort is stable, so equal priorities retain caller order.
        optional.sort(key=lambda entry: entry.item.priority, reverse=True)
        for entry in optional:
            if used + entry.estimated_tokens <= budget:
                included_ids.add(entry.item.item_id)
                used += entry.estimated_tokens

        included = tuple(entry for entry in measured if entry.item.item_id in included_ids)
        dropped = tuple(entry for entry in measured if entry.item.item_id not in included_ids)
        return BudgetPlan(budget, used, budget - used, included, dropped)

"""Deterministic context admission under a finite input-token budget."""

from dataclasses import dataclass
from typing import Sequence

from app.token_counting import TokenCounter


@dataclass(frozen=True)
class BudgetConfig:
    context_window_tokens: int
    reserved_output_tokens: int
    safety_margin_tokens: int = 0
    per_item_overhead_tokens: int = 0

    def __post_init__(self) -> None:
        values = (
            self.context_window_tokens,
            self.reserved_output_tokens,
            self.safety_margin_tokens,
            self.per_item_overhead_tokens,
        )
        if any(value < 0 for value in values):
            raise ValueError("token budget values cannot be negative")
        if self.context_window_tokens == 0:
            raise ValueError("context_window_tokens must be greater than zero")
        if self.reserved_output_tokens + self.safety_margin_tokens >= self.context_window_tokens:
            raise ValueError("output reserve plus safety margin must be smaller than context window")

    @property
    def available_input_tokens(self) -> int:
        return (
            self.context_window_tokens
            - self.reserved_output_tokens
            - self.safety_margin_tokens
        )


@dataclass(frozen=True)
class ContextItem:
    item_id: str
    kind: str
    text: str
    priority: int = 0
    mandatory: bool = False

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise ValueError("item_id cannot be empty")
        if not self.kind.strip():
            raise ValueError("kind cannot be empty")
        if not isinstance(self.text, str):
            raise TypeError("context text must be a string")


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
    """Raised when required context cannot fit without violating the budget."""


class BudgetPlanner:
    def __init__(self, counter: TokenCounter, config: BudgetConfig) -> None:
        self._counter = counter
        self._config = config

    def plan(self, items: Sequence[ContextItem]) -> BudgetPlan:
        ids = [item.item_id for item in items]
        if len(ids) != len(set(ids)):
            raise ValueError("context item IDs must be unique")

        measured = [
            PlannedItem(
                item=item,
                estimated_tokens=(
                    self._counter.count(item.text)
                    + self._config.per_item_overhead_tokens
                ),
            )
            for item in items
        ]
        if any(entry.estimated_tokens < 0 for entry in measured):
            raise ValueError("token counter returned a negative count")

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

        optional.sort(key=lambda entry: entry.item.priority, reverse=True)
        for entry in optional:
            if used + entry.estimated_tokens <= budget:
                included_ids.add(entry.item.item_id)
                used += entry.estimated_tokens

        included = tuple(entry for entry in measured if entry.item.item_id in included_ids)
        dropped = tuple(entry for entry in measured if entry.item.item_id not in included_ids)
        return BudgetPlan(
            available_input_tokens=budget,
            estimated_input_tokens=used,
            remaining_input_tokens=budget - used,
            included=included,
            dropped=dropped,
        )

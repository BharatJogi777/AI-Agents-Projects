"""Recency-based context truncation that preserves complete conversation turns."""

from dataclasses import dataclass
from typing import Literal, Sequence

from app.token_counting import TokenCounter

Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True, slots=True)
class ContextMessage:
    role: Role
    content: str
    turn_id: str | None = None

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise ValueError("message content cannot be empty")
        if self.role == "system" and self.turn_id is not None:
            raise ValueError("system messages cannot belong to a conversation turn")
        if self.role != "system" and not self.turn_id:
            raise ValueError("conversation messages require a turn_id")


@dataclass(frozen=True, slots=True)
class TruncationConfig:
    context_window_tokens: int
    reserved_output_tokens: int
    safety_margin_tokens: int = 0
    per_message_overhead_tokens: int = 0

    def __post_init__(self) -> None:
        values = (
            self.context_window_tokens,
            self.reserved_output_tokens,
            self.safety_margin_tokens,
            self.per_message_overhead_tokens,
        )
        if any(value < 0 for value in values):
            raise ValueError("token limits cannot be negative")
        if self.context_window_tokens == 0:
            raise ValueError("context_window_tokens must be positive")
        if self.reserved_output_tokens + self.safety_margin_tokens >= self.context_window_tokens:
            raise ValueError("reserved output and safety margin must be below context window")

    @property
    def input_budget(self) -> int:
        return self.context_window_tokens - self.reserved_output_tokens - self.safety_margin_tokens


@dataclass(frozen=True)
class TruncationResult:
    input_budget: int
    estimated_tokens: int
    remaining_tokens: int
    messages: tuple[ContextMessage, ...]
    dropped_turn_ids: tuple[str, ...]


class MandatoryContextTooLarge(ValueError):
    """System instructions and the current user message exceed the input budget."""


class InvalidConversation(ValueError):
    """The supplied history is not a sequence of complete user/assistant turns."""


class ContextTruncator:
    """Keep all system messages, the current user message, and newest whole turns.

    Input order must be: zero or more system messages, zero or more completed
    user/assistant turns, and one final pending user message. Tool transcripts
    and multi-message assistant turns need a richer message model and are
    intentionally outside this project's scope.
    """

    def __init__(self, counter: TokenCounter, config: TruncationConfig) -> None:
        self._counter = counter
        self._config = config

    def truncate(self, messages: Sequence[ContextMessage]) -> TruncationResult:
        if not messages:
            raise InvalidConversation("at least a current user message is required")

        system_messages: list[ContextMessage] = []
        turns: list[tuple[str, list[ContextMessage]]] = []
        current_user: ContextMessage | None = None
        phase = "system"
        index = 0

        while index < len(messages):
            message = messages[index]
            if message.role == "system":
                if phase != "system":
                    raise InvalidConversation("system messages must appear before conversation turns")
                system_messages.append(message)
                index += 1
                continue

            phase = "conversation"
            if message.role == "user":
                if index == len(messages) - 1:
                    if current_user is not None:
                        raise InvalidConversation("multiple pending user messages")
                    current_user = message
                    index += 1
                    break

                if index + 1 >= len(messages) or messages[index + 1].role != "assistant":
                    raise InvalidConversation("each completed user turn must have an assistant response")
                assistant = messages[index + 1]
                if assistant.turn_id != message.turn_id:
                    raise InvalidConversation("user and assistant messages in a turn must share turn_id")
                if any(turn_id == message.turn_id for turn_id, _ in turns):
                    raise InvalidConversation("turn_id values must be unique")
                turns.append((message.turn_id or "", [message, assistant]))
                index += 2
                continue

            raise InvalidConversation("assistant message cannot appear without its user message")

        if index != len(messages) or current_user is None:
            raise InvalidConversation("history must end with exactly one pending current user message")

        mandatory = system_messages + [current_user]
        mandatory_tokens = sum(self._measure(message) for message in mandatory)
        budget = self._config.input_budget
        if mandatory_tokens > budget:
            raise MandatoryContextTooLarge(
                f"mandatory context requires {mandatory_tokens} tokens, budget is {budget}"
            )

        selected_ids: set[str] = set()
        used = mandatory_tokens
        dropped_ids: list[str] = []

        # Walk backward to retain the most recent complete turns. Once a turn
        # does not fit, older turns cannot be considered: recency stays contiguous.
        for turn_id, turn_messages in reversed(turns):
            turn_tokens = sum(self._measure(message) for message in turn_messages)
            if used + turn_tokens <= budget:
                selected_ids.add(turn_id)
                used += turn_tokens
            else:
                dropped_ids.extend(
                    older_id for older_id, _ in turns if older_id not in selected_ids and older_id not in dropped_ids
                )
                break

        retained = tuple(
            message
            for message in messages
            if message.role == "system"
            or message is current_user
            or (message.turn_id in selected_ids)
        )
        return TruncationResult(
            input_budget=budget,
            estimated_tokens=used,
            remaining_tokens=budget - used,
            messages=retained,
            dropped_turn_ids=tuple(dropped_ids),
        )

    def _measure(self, message: ContextMessage) -> int:
        count = self._counter.count(message.content)
        if count < 0:
            raise ValueError("token counter returned a negative count")
        return count + self._config.per_message_overhead_tokens

"""Budget-aware conversation truncation with atomic tool exchanges."""
from dataclasses import dataclass
from typing import Literal, Sequence
from app.token_counting import TokenCounter

Role = Literal["system", "user", "assistant", "tool"]

@dataclass(frozen=True, slots=True)
class ContextMessage:
    role: Role
    content: str
    turn_id: str | None = None
    tool_call_id: str | None = None
    tool_call_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.role not in ("system", "user", "assistant", "tool"):
            raise ValueError("unsupported message role")
        if not isinstance(self.content, str):
            raise ValueError("message content must be a string")
        if self.role != "assistant" and not self.content.strip():
            raise ValueError("non-assistant message content cannot be empty")
        if self.role == "system":
            if self.turn_id is not None or self.tool_call_id or self.tool_call_ids:
                raise ValueError("system messages cannot contain turn or tool metadata")
        elif not self.turn_id or not self.turn_id.strip():
            raise ValueError("conversation messages require a non-empty turn_id")
        if self.role == "tool" and not self.tool_call_id:
            raise ValueError("tool result requires tool_call_id")
        if self.role != "tool" and self.tool_call_id is not None:
            raise ValueError("tool_call_id is only valid on tool result messages")
        if self.role != "assistant" and self.tool_call_ids:
            raise ValueError("tool_call_ids are only valid on assistant messages")
        if len(set(self.tool_call_ids)) != len(self.tool_call_ids) or any(not x for x in self.tool_call_ids):
            raise ValueError("assistant tool_call_ids must be unique and non-empty")

@dataclass(frozen=True, slots=True)
class TruncationConfig:
    context_window_tokens: int
    reserved_output_tokens: int
    safety_margin_tokens: int = 0
    per_message_overhead_tokens: int = 0

    def __post_init__(self) -> None:
        values = (self.context_window_tokens, self.reserved_output_tokens, self.safety_margin_tokens, self.per_message_overhead_tokens)
        if any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in values):
            raise ValueError("token limits must be non-negative integers")
        if self.context_window_tokens == 0:
            raise ValueError("context_window_tokens must be positive")
        if self.reserved_output_tokens + self.safety_margin_tokens >= self.context_window_tokens:
            raise ValueError("reserved output and safety margin must be below context window")

    @property
    def input_budget(self) -> int:
        return self.context_window_tokens - self.reserved_output_tokens - self.safety_margin_tokens

@dataclass(frozen=True, slots=True)
class TruncationResult:
    input_budget: int
    estimated_tokens: int
    remaining_tokens: int
    messages: tuple[ContextMessage, ...]
    dropped_turn_ids: tuple[str, ...]

class MandatoryContextTooLarge(ValueError):
    """Mandatory system instructions and current request exceed the input budget."""

class InvalidConversation(ValueError):
    """Conversation history contains an incomplete or invalid turn/tool exchange."""

class ContextTruncator:
    """Keep system instructions, current request, and newest complete turns."""
    def __init__(self, counter: TokenCounter, config: TruncationConfig) -> None:
        self._counter = counter
        self._config = config

    def truncate(self, messages: Sequence[ContextMessage]) -> TruncationResult:
        if not messages:
            raise InvalidConversation("at least a current user message is required")
        system, turns, current = [], [], None
        index, in_history = 0, False
        while index < len(messages):
            message = messages[index]
            if message.role == "system":
                if in_history:
                    raise InvalidConversation("system messages must precede conversation history")
                system.append(message)
                index += 1
                continue
            in_history = True
            if message.role != "user":
                raise InvalidConversation("each turn must begin with a user message")
            if index == len(messages) - 1:
                current = message
                index += 1
                break
            turn_id = message.turn_id or ""
            if any(existing == turn_id for existing, _ in turns):
                raise InvalidConversation("turn_id values must be unique")
            turn, pending, final_seen = [message], set(), False
            index += 1
            while index < len(messages) and messages[index].role != "user":
                item = messages[index]
                if item.turn_id != turn_id:
                    raise InvalidConversation("all messages in a turn must share turn_id")
                if final_seen:
                    raise InvalidConversation("no messages may follow the final assistant answer")
                if item.role == "assistant":
                    if pending:
                        raise InvalidConversation("tool results must resolve before another assistant message")
                    if item.tool_call_ids:
                        pending.update(item.tool_call_ids)
                    else:
                        final_seen = True
                elif item.role == "tool":
                    if not pending or item.tool_call_id not in pending:
                        raise InvalidConversation("tool result has no matching pending tool call")
                    pending.remove(item.tool_call_id or "")
                else:
                    raise InvalidConversation("unexpected role inside a completed turn")
                turn.append(item)
                index += 1
            if pending:
                raise InvalidConversation("completed turn contains unresolved tool calls")
            if not final_seen:
                raise InvalidConversation("completed turn must end with an assistant answer")
            turns.append((turn_id, turn))
        if index != len(messages) or current is None:
            raise InvalidConversation("history must end with exactly one pending current user message")
        if any(turn_id == current.turn_id for turn_id, _ in turns):
            raise InvalidConversation("current user turn_id must be unique")

        mandatory = system + [current]
        mandatory_tokens = sum(self._measure(item) for item in mandatory)
        budget = self._config.input_budget
        if mandatory_tokens > budget:
            raise MandatoryContextTooLarge(f"mandatory context requires {mandatory_tokens} tokens, budget is {budget}")
        selected, used, dropped = set(), mandatory_tokens, []
        for turn_id, turn in reversed(turns):
            cost = sum(self._measure(item) for item in turn)
            if used + cost <= budget:
                selected.add(turn_id)
                used += cost
            else:
                dropped.extend(old_id for old_id, _ in turns if old_id not in selected and old_id not in dropped)
                break
        retained = tuple(item for item in messages if item.role == "system" or item is current or item.turn_id in selected)
        measured = sum(self._measure(item) for item in retained)
        if measured > budget:
            raise RuntimeError("internal budget invariant violated")
        return TruncationResult(budget, measured, budget - measured, retained, tuple(dropped))

    def _measure(self, message: ContextMessage) -> int:
        count = self._counter.count(message.content)
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError("token counter must return a non-negative integer")
        return count + self._config.per_message_overhead_tokens

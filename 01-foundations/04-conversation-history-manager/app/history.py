"""Session-scoped, bounded chat history with explicit turn ordering."""

from dataclasses import dataclass
from typing import Literal


Role = Literal["user", "assistant"]


@dataclass(frozen=True, slots=True)
class Message:
    role: Role
    content: str


class ConversationHistory:
    """In-memory history for one conversation.

    The system prompt is pinned and is never evicted. User/assistant messages
    are stored as complete turns; trimming removes oldest complete turns only.
    This class is intentionally not a persistent cross-session memory store.
    """

    def __init__(
        self,
        *,
        session_id: str,
        system_prompt: str,
        max_turns: int = 10,
        max_message_chars: int = 8_000,
    ) -> None:
        if not session_id.strip():
            raise ValueError("session_id cannot be empty")
        if not system_prompt.strip():
            raise ValueError("system_prompt cannot be empty")
        if max_turns < 1:
            raise ValueError("max_turns must be at least 1")
        if max_message_chars < 1:
            raise ValueError("max_message_chars must be positive")

        self.session_id = session_id
        self._system_prompt = system_prompt.strip()
        self._max_turns = max_turns
        self._max_message_chars = max_message_chars
        self._turns: list[tuple[Message, Message]] = []
        self._pending_user: Message | None = None

    def add_user_message(self, content: str) -> None:
        self._validate_content(content)
        if self._pending_user is not None:
            raise ValueError("assistant response is required before the next user message")
        self._pending_user = Message(role="user", content=content)

    def add_assistant_message(self, content: str) -> None:
        self._validate_content(content)
        if self._pending_user is None:
            raise ValueError("cannot add an assistant message without a pending user message")

        self._turns.append(
            (self._pending_user, Message(role="assistant", content=content))
        )
        self._pending_user = None
        overflow = len(self._turns) - self._max_turns
        if overflow > 0:
            del self._turns[:overflow]

    def build_messages(self, *, include_pending_user: bool = True) -> list[dict[str, str]]:
        """Build provider-neutral messages without exposing internal storage."""
        result = [{"role": "system", "content": self._system_prompt}]
        for user_message, assistant_message in self._turns:
            result.append({"role": user_message.role, "content": user_message.content})
            result.append(
                {"role": assistant_message.role, "content": assistant_message.content}
            )
        if include_pending_user and self._pending_user is not None:
            result.append(
                {"role": "user", "content": self._pending_user.content}
            )
        return result

    def clear(self) -> None:
        """Clear this session's turns while retaining its system prompt."""
        self._turns.clear()
        self._pending_user = None

    @property
    def completed_turns(self) -> int:
        return len(self._turns)

    def _validate_content(self, content: str) -> None:
        if not content.strip():
            raise ValueError("message content cannot be empty")
        if len(content) > self._max_message_chars:
            raise ValueError(
                f"message exceeds the {self._max_message_chars}-character limit"
            )

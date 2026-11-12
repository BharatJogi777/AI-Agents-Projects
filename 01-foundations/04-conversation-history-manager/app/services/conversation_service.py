from uuid import uuid4
from app.storage.repository import ConversationRepository, InvalidMessageOrder

class ConversationNotFound(Exception):
    pass

class ConversationConflict(Exception):
    pass

class ConversationService:
    def __init__(self, repository: ConversationRepository, max_message_chars=8000):
        self.repository = repository
        self.max_message_chars = max_message_chars

    def create(self, system_prompt, max_turns=10):
        prompt = system_prompt.strip()
        if not prompt:
            raise ValueError("system_prompt cannot be blank")
        return self.repository.create(str(uuid4()), prompt, max_turns)

    def _require(self, conversation_id):
        item = self.repository.get(conversation_id)
        if item is None:
            raise ConversationNotFound(conversation_id)
        return item

    def _validate(self, content):
        if not content.strip():
            raise ValueError("message content cannot be blank")
        if len(content) > self.max_message_chars:
            raise ValueError(f"message exceeds {self.max_message_chars} characters")

    def _append(self, conversation_id, role, content):
        try:
            return self.repository.append_checked(conversation_id, role, content)
        except KeyError as exc:
            raise ConversationNotFound(conversation_id) from exc
        except InvalidMessageOrder as exc:
            if role == "user":
                message = "assistant response is required before the next user message"
            else:
                message = "assistant message requires a pending user message"
            raise ConversationConflict(message) from exc

    def append_user(self, conversation_id, content):
        self._require(conversation_id)
        self._validate(content)
        return self._append(conversation_id, "user", content)

    def append_assistant(self, conversation_id, content):
        item = self._require(conversation_id)
        self._validate(content)
        message = self._append(conversation_id, "assistant", content)
        self.repository.trim_completed_turns(conversation_id, item["max_turns"])
        return message

    def history(self, conversation_id, limit=100, offset=0):
        item = self._require(conversation_id)
        return {"conversation_id": conversation_id, "system_prompt": item["system_prompt"],
                "messages": self.repository.list_messages(conversation_id, limit, offset),
                "limit": limit, "offset": offset}

    def clear(self, conversation_id):
        self._require(conversation_id)
        self.repository.clear(conversation_id)

    def delete(self, conversation_id):
        self._require(conversation_id)
        return self.repository.delete(conversation_id)

    def list(self, limit=50, offset=0):
        return self.repository.list_conversations(limit, offset)

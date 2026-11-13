"""Validated message envelopes and an in-memory deduplicating inbox."""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any
from uuid import uuid4

@dataclass(frozen=True)
class MessageEnvelope:
    message_id: str
    correlation_id: str
    sender: str
    recipient: str
    kind: str
    payload: dict[str, Any]
    created_at: datetime
    expires_at: datetime | None = None

    @classmethod
    def create(cls, sender: str, recipient: str, kind: str, payload: dict,
               correlation_id: str | None = None, ttl_seconds: int | None = None):
        if not sender or not recipient or not kind:
            raise ValueError("sender, recipient and kind are required")
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")
        if ttl_seconds is not None and ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        now = datetime.now(timezone.utc)
        return cls(str(uuid4()), correlation_id or str(uuid4()), sender,
                   recipient, kind, payload, now,
                   now + timedelta(seconds=ttl_seconds) if ttl_seconds else None)

    def validate(self, now: datetime | None = None) -> None:
        if not self.message_id or not self.correlation_id:
            raise ValueError("message and correlation IDs are required")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")
        if self.expires_at and self.expires_at <= (now or datetime.now(timezone.utc)):
            raise ValueError("message has expired")

class Inbox:
    def __init__(self, recipient: str):
        if not recipient:
            raise ValueError("recipient is required")
        self.recipient = recipient
        self._messages: dict[str, MessageEnvelope] = {}

    def deliver(self, message: MessageEnvelope, now: datetime | None = None) -> bool:
        message.validate(now)
        if message.recipient != self.recipient:
            raise ValueError("message addressed to another agent")
        if message.message_id in self._messages:
            return False
        self._messages[message.message_id] = message
        return True

    def receive(self, kind: str | None = None) -> list[MessageEnvelope]:
        messages = [m for m in self._messages.values() if kind is None or m.kind == kind]
        return sorted(messages, key=lambda m: m.created_at)

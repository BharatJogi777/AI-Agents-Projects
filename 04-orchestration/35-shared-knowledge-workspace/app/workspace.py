"""Attributed shared knowledge store with revisions and topic lookup."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class Knowledge:
    item_id: str
    topic: str
    content: Any
    source_agent: str
    confidence: float
    revision: int
    updated_at: datetime

class KnowledgeWorkspace:
    def __init__(self):
        self._items: dict[str, Knowledge] = {}

    def publish(self, item_id: str, topic: str, content: Any, source_agent: str,
                confidence: float, expected_revision: int | None = None) -> Knowledge:
        if not all((item_id, topic, source_agent)):
            raise ValueError("item_id, topic and source_agent are required")
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        current = self._items.get(item_id)
        revision = current.revision if current else 0
        if expected_revision is not None and expected_revision != revision:
            raise RuntimeError(f"revision conflict: expected {expected_revision}, found {revision}")
        item = Knowledge(item_id, topic, content, source_agent, confidence,
                         revision + 1, datetime.now(timezone.utc))
        self._items[item_id] = item
        return item

    def get(self, item_id: str) -> Knowledge | None:
        return self._items.get(item_id)

    def search(self, topic: str, minimum_confidence: float = 0.0) -> tuple[Knowledge, ...]:
        if not topic:
            raise ValueError("topic is required")
        if not 0 <= minimum_confidence <= 1:
            raise ValueError("minimum_confidence must be between 0 and 1")
        matches = [item for item in self._items.values()
                   if item.topic == topic and item.confidence >= minimum_confidence]
        return tuple(sorted(matches, key=lambda item: (-item.confidence, item.item_id)))

    def remove(self, item_id: str) -> bool:
        return self._items.pop(item_id, None) is not None

"""Compatibility facade. New code should import conversation_memory."""
from conversation_memory import Message,ShortTermMemory
__all__=["Message","ShortTermMemory"]

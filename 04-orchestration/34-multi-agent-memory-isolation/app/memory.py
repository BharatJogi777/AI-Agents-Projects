"""Tenant-isolated agent memory with explicit scoped access."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class MemoryRecord:
    key: str
    value: Any
    agent_id: str
    namespace: str

class IsolatedMemory:
    def __init__(self):
        self._records: dict[tuple[str, str, str], MemoryRecord] = {}

    def put(self, agent_id: str, namespace: str, key: str, value: Any) -> None:
        if not all((agent_id, namespace, key)):
            raise ValueError("agent_id, namespace and key are required")
        self._records[(agent_id, namespace, key)] = MemoryRecord(key, value, agent_id, namespace)

    def get(self, agent_id: str, namespace: str, key: str) -> MemoryRecord | None:
        if not all((agent_id, namespace, key)):
            raise ValueError("agent_id, namespace and key are required")
        return self._records.get((agent_id, namespace, key))

    def list_namespace(self, agent_id: str, namespace: str) -> tuple[MemoryRecord, ...]:
        return tuple(r for (owner, space, _), r in self._records.items()
                     if owner == agent_id and space == namespace)

    def delete(self, agent_id: str, namespace: str, key: str) -> bool:
        return self._records.pop((agent_id, namespace, key), None) is not None

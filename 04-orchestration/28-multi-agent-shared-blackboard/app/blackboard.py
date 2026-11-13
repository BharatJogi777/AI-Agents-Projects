"""Versioned shared blackboard with optimistic concurrency control."""
from dataclasses import dataclass, field
from threading import RLock
from typing import Any

@dataclass(frozen=True)
class Entry:
    key: str
    value: Any
    version: int
    author: str

@dataclass
class Blackboard:
    _entries: dict[str, Entry] = field(default_factory=dict)
    _history: list[Entry] = field(default_factory=list)
    _lock: RLock = field(default_factory=RLock, repr=False)

    def read(self, key: str) -> Entry | None:
        with self._lock:
            return self._entries.get(key)

    def write(self, key: str, value: Any, author: str, expected_version: int | None = None) -> Entry:
        if not key or not author:
            raise ValueError("key and author are required")
        with self._lock:
            current = self._entries.get(key)
            actual = current.version if current else 0
            if expected_version is not None and expected_version != actual:
                raise RuntimeError(f"version conflict: expected {expected_version}, found {actual}")
            entry = Entry(key, value, actual + 1, author)
            self._entries[key] = entry
            self._history.append(entry)
            return entry

    def observe(self, key: str, value: Any, author: str) -> Entry:
        """Append an observation without overwriting the shared current value."""
        if not key or not author:
            raise ValueError("key and author are required")
        with self._lock:
            prior = [e for e in self._history if e.key == key]
            entry = Entry(key, value, len(prior) + 1, author)
            self._history.append(entry)
            return entry

    def history(self, key: str | None = None) -> tuple[Entry, ...]:
        with self._lock:
            return tuple(e for e in self._history if key is None or e.key == key)

    def snapshot(self) -> dict[str, Entry]:
        with self._lock:
            return dict(self._entries)

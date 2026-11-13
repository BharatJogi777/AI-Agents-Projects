"""Append-only JSONL audit sink with explicit field allowlisting."""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Mapping

_ALLOWED = {"request_id", "principal", "tool", "decision", "duration_ms", "status"}

class JsonlAuditLog:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._lock = Lock()

    def write(self, event: Mapping[str, object]) -> None:
        safe = {key: event[key] for key in _ALLOWED if key in event}
        for key in ("request_id", "principal", "tool", "decision", "status"):
            if key in safe and not isinstance(safe[key], str):
                raise TypeError(f"{key} must be a string")
        if "duration_ms" in safe and (not isinstance(safe["duration_ms"], (int, float)) or safe["duration_ms"] < 0):
            raise ValueError("duration_ms must be a non-negative number")
        record = {"timestamp": datetime.now(timezone.utc).isoformat(), **safe}
        line = json.dumps(record, separators=(",", ":"), ensure_ascii=False)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            fd = os.open(self.path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
            try:
                os.write(fd, (line + "\n").encode("utf-8"))
            finally:
                os.close(fd)

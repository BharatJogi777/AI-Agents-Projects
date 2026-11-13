import json
import sqlite3
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class StoredState:
    workflow_id: str
    version: int
    state: dict[str, Any]

class SQLiteStateStore:
    def __init__(self, path: str):
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS workflow_state (
            workflow_id TEXT PRIMARY KEY, version INTEGER NOT NULL, payload TEXT NOT NULL)""")
        self.db.commit()

    def save(self, workflow_id: str, state: dict[str, Any], expected_version: int | None = None) -> StoredState:
        if not workflow_id.strip() or not isinstance(state, dict): raise ValueError("workflow id and object state required")
        payload = json.dumps(state, separators=(",", ":"), sort_keys=True)
        row = self.db.execute("SELECT version FROM workflow_state WHERE workflow_id=?", (workflow_id,)).fetchone()
        if row is None:
            if expected_version not in (None, 0): raise RuntimeError("state version conflict")
            version = 1
            self.db.execute("INSERT INTO workflow_state VALUES (?, ?, ?)", (workflow_id, version, payload))
        else:
            current = row[0]
            if expected_version is None or current != expected_version: raise RuntimeError("state version conflict")
            version = current + 1
            changed = self.db.execute("UPDATE workflow_state SET version=?, payload=? WHERE workflow_id=? AND version=?", (version, payload, workflow_id, current)).rowcount
            if changed != 1: raise RuntimeError("state version conflict")
        self.db.commit()
        return StoredState(workflow_id, version, dict(state))

    def load(self, workflow_id: str) -> StoredState | None:
        row = self.db.execute("SELECT version, payload FROM workflow_state WHERE workflow_id=?", (workflow_id,)).fetchone()
        if row is None: return None
        return StoredState(workflow_id, row[0], json.loads(row[1]))

    def close(self) -> None:
        self.db.close()

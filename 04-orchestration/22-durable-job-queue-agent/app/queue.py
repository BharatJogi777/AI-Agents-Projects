import json, sqlite3
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Job:
    job_id: str
    payload: dict[str, Any]
    status: str
    attempts: int

class SQLiteJobQueue:
    def __init__(self, path: str):
        self.db=sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("""CREATE TABLE IF NOT EXISTS jobs(
            job_id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0, result TEXT)""")

    def enqueue(self, job_id: str, payload: dict[str, Any]) -> None:
        if not job_id.strip() or not isinstance(payload,dict): raise ValueError("job id and object payload required")
        self.db.execute("INSERT INTO jobs(job_id,payload,status) VALUES(?,?,?)",
                        (job_id,json.dumps(payload,sort_keys=True),"queued"))

    def claim(self) -> Job | None:
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row=self.db.execute("SELECT job_id,payload,attempts FROM jobs WHERE status='queued' ORDER BY rowid LIMIT 1").fetchone()
            if row is None:
                self.db.execute("COMMIT"); return None
            self.db.execute("UPDATE jobs SET status='running',attempts=attempts+1 WHERE job_id=?",(row[0],))
            self.db.execute("COMMIT")
            return Job(row[0],json.loads(row[1]),"running",row[2]+1)
        except Exception:
            self.db.execute("ROLLBACK"); raise

    def complete(self, job_id: str, result: Any) -> None:
        cur=self.db.execute("UPDATE jobs SET status='done',result=? WHERE job_id=? AND status='running'",(json.dumps(result),job_id))
        if cur.rowcount != 1: raise RuntimeError("job is not running")

    def retry(self, job_id: str) -> None:
        cur=self.db.execute("UPDATE jobs SET status='queued' WHERE job_id=? AND status='running'",(job_id,))
        if cur.rowcount != 1: raise RuntimeError("job is not running")

    def close(self): self.db.close()

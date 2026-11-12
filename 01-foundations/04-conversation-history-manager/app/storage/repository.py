from datetime import datetime, timezone
from app.storage.database import Database

def utc_now():
    return datetime.now(timezone.utc).isoformat()

class ConversationRepository:
    def __init__(self, database: Database):
        self.database = database

    def create(self, conversation_id, system_prompt, max_turns):
        now = utc_now()
        with self.database.connect() as db:
            db.execute("INSERT INTO conversations VALUES (?,?,?,?,?)",
                       (conversation_id, system_prompt, max_turns, now, now))
            return dict(db.execute("SELECT * FROM conversations WHERE id=?",
                                   (conversation_id,)).fetchone())

    def get(self, conversation_id):
        with self.database.connect() as db:
            row = db.execute("SELECT * FROM conversations WHERE id=?",
                             (conversation_id,)).fetchone()
            return dict(row) if row else None

    def append(self, conversation_id, role, content):
        now = utc_now()
        with self.database.connect() as db:
            cursor = db.execute(
                "INSERT INTO messages(conversation_id,role,content,created_at) VALUES(?,?,?,?)",
                (conversation_id, role, content, now))
            db.execute("UPDATE conversations SET updated_at=? WHERE id=?",
                       (now, conversation_id))
            return dict(db.execute("SELECT * FROM messages WHERE id=?",
                                   (cursor.lastrowid,)).fetchone())

    def last_role(self, conversation_id):
        with self.database.connect() as db:
            row = db.execute("SELECT role FROM messages WHERE conversation_id=? ORDER BY id DESC LIMIT 1",
                             (conversation_id,)).fetchone()
            return row["role"] if row else None

    def list_messages(self, conversation_id, limit, offset):
        with self.database.connect() as db:
            rows = db.execute(
                "SELECT * FROM messages WHERE conversation_id=? ORDER BY id LIMIT ? OFFSET ?",
                (conversation_id, limit, offset)).fetchall()
            return [dict(row) for row in rows]

    def trim_completed_turns(self, conversation_id, max_turns):
        with self.database.connect() as db:
            rows = db.execute("SELECT id,role FROM messages WHERE conversation_id=? ORDER BY id",
                              (conversation_id,)).fetchall()
            pairs, pending = [], None
            for row in rows:
                if row["role"] == "user":
                    pending = row["id"]
                elif pending is not None:
                    pairs.append((pending, row["id"]))
                    pending = None
            excess = len(pairs) - max_turns
            if excess > 0:
                ids = [item for pair in pairs[:excess] for item in pair]
                marks = ",".join("?" for _ in ids)
                db.execute(f"DELETE FROM messages WHERE id IN ({marks})", ids)

    def clear(self, conversation_id):
        with self.database.connect() as db:
            db.execute("DELETE FROM messages WHERE conversation_id=?", (conversation_id,))

    def delete(self, conversation_id):
        with self.database.connect() as db:
            return db.execute("DELETE FROM conversations WHERE id=?", (conversation_id,)).rowcount > 0

    def list_conversations(self, limit, offset):
        with self.database.connect() as db:
            rows = db.execute(
                """SELECT c.id,c.system_prompt,c.max_turns,c.created_at,c.updated_at,
                          COUNT(m.id) AS message_count
                   FROM conversations c LEFT JOIN messages m ON m.conversation_id=c.id
                   GROUP BY c.id ORDER BY c.updated_at DESC,c.id LIMIT ? OFFSET ?""",
                (limit, offset)).fetchall()
            return [dict(row) for row in rows]

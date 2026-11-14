"""Structure meeting notes into actions, decisions, and open questions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Note:
    text: str
    kind: str
    owner: str | None = None
    due_date: str | None = None

def build_follow_up(notes: list[Note]) -> dict:
    allowed = {"action", "decision", "question"}
    result = {"actions": [], "decisions": [], "questions": []}
    for note in notes:
        if not note.text.strip():
            raise ValueError("note text must be non-empty")
        if note.kind not in allowed:
            raise ValueError(f"unsupported note kind: {note.kind}")
        entry = {"text": note.text.strip()}
        if note.kind == "action":
            entry.update({"owner": note.owner, "due_date": note.due_date, "needs_owner_confirmation": note.owner is None, "needs_deadline_confirmation": note.due_date is None})
            result["actions"].append(entry)
        else:
            result["decisions" if note.kind == "decision" else "questions"].append(entry)
    return result

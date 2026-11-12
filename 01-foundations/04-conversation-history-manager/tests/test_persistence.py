from app.services.conversation_service import ConversationService
from app.storage.database import Database
from app.storage.repository import ConversationRepository

def test_messages_survive_service_recreation(tmp_path):
    path = tmp_path / "persistent.db"
    first = ConversationService(ConversationRepository(Database(path)))
    session = first.create("System prompt", max_turns=3)
    first.append_user(session["id"], "Persist this")
    first.append_assistant(session["id"], "Stored answer")
    restarted = ConversationService(ConversationRepository(Database(path)))
    history = restarted.history(session["id"])
    assert [m["content"] for m in history["messages"]] == ["Persist this", "Stored answer"]

def test_sessions_are_isolated(tmp_path):
    service = ConversationService(ConversationRepository(Database(tmp_path / "isolation.db")))
    first, second = service.create("System A"), service.create("System B")
    service.append_user(first["id"], "private A")
    service.append_assistant(first["id"], "answer A")
    assert service.history(second["id"])["messages"] == []

def test_pending_user_turn_is_not_trimmed(tmp_path):
    service = ConversationService(ConversationRepository(Database(tmp_path / "pending.db")))
    session = service.create("system", max_turns=1)
    service.append_user(session["id"], "Q1")
    service.append_assistant(session["id"], "A1")
    service.append_user(session["id"], "Q2")
    history = service.history(session["id"])["messages"]
    assert [m["content"] for m in history] == ["Q1", "A1", "Q2"]

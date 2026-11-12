import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.services.conversation_service import ConversationService
from app.storage.database import Database
from app.storage.repository import ConversationRepository

@pytest.fixture
def service(tmp_path):
    return ConversationService(ConversationRepository(Database(tmp_path / "test.db")), max_message_chars=100)

@pytest.fixture
def client(service):
    return TestClient(create_app(service))

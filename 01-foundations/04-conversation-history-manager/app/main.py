import os
from functools import lru_cache
from fastapi import FastAPI
from app.storage.database import Database
from app.storage.repository import ConversationRepository
from app.services.conversation_service import ConversationService

@lru_cache(maxsize=1)
def get_service():
    database = Database(os.getenv("CONVERSATION_DB_PATH", "./data/conversations.db"))
    return ConversationService(ConversationRepository(database))

def create_app(service=None):
    application = FastAPI(title="Conversation History Manager", version="1.0.0")
    if service is not None:
        application.dependency_overrides[get_service] = lambda: service
    from app.api.routes.conversations import router
    application.include_router(router, prefix="/api/v1")

    @application.get("/health/live", tags=["health"])
    def liveness():
        return {"status": "alive"}
    return application

app = create_app()

from app.agent import ToolCallingAgent
from app.api import create_app
from app.config import Settings
from app.llm import OllamaChatClient

settings = Settings()
agent = ToolCallingAgent(
    client=OllamaChatClient(settings.base_url, settings.model, settings.timeout_seconds),
    max_steps=settings.max_steps,
)
app = create_app(agent)

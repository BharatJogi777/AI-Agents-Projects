from app.agent import ToolCallingAgent
from app.api import create_app
from app.config import Settings
from app.llm import OllamaChatClient

settings = Settings()
llm_client = OllamaChatClient(
    settings.base_url,
    settings.model,
    settings.timeout_seconds,
)
agent = ToolCallingAgent(client=llm_client, max_steps=settings.max_steps)
app = create_app(agent, readiness_check=llm_client.is_ready)

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1").rstrip("/")
    model: str = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    max_steps: int = int(os.getenv("AGENT_MAX_STEPS", "5"))
    timeout_seconds: float = float(os.getenv("HTTP_TIMEOUT_SECONDS", "60"))

    def __post_init__(self) -> None:
        if self.max_steps < 1:
            raise ValueError("AGENT_MAX_STEPS must be at least 1")
        if self.timeout_seconds <= 0:
            raise ValueError("HTTP_TIMEOUT_SECONDS must be positive")

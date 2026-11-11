from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model: str = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    timeout_seconds: float = float(os.getenv("HTTP_TIMEOUT_SECONDS", "60"))

    def __post_init__(self) -> None:
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError("OLLAMA_BASE_URL must be an HTTP(S) URL")
        if not self.model.strip():
            raise ValueError("OLLAMA_MODEL cannot be empty")
        if self.timeout_seconds <= 0:
            raise ValueError("HTTP_TIMEOUT_SECONDS must be positive")

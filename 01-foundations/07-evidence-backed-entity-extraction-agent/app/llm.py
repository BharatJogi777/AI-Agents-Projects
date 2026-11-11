from typing import Any

import httpx


class OllamaClient:
    """Ollama native chat client with JSON Schema constrained output."""

    def __init__(self, base_url: str, model: str, timeout_seconds: float = 60) -> None:
        self.url = f"{base_url.rstrip('/')}/api/chat"
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate_structured(
        self,
        messages: list[dict[str, str]],
        json_schema: dict[str, Any],
    ) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "format": json_schema,
            "stream": False,
            "options": {"temperature": 0},
        }
        try:
            response = httpx.post(self.url, json=payload, timeout=self.timeout_seconds)
            response.raise_for_status()
            data = response.json()
        except httpx.TimeoutException as exc:
            raise RuntimeError("Ollama request timed out") from exc
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc
        except ValueError as exc:
            raise RuntimeError("Ollama returned an invalid HTTP response") from exc

        try:
            content = data["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError("Ollama response did not contain message.content") from exc
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Ollama returned empty structured content")
        return content

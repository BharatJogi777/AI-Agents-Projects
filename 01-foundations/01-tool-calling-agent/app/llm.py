from typing import Any

import httpx


class OllamaChatClient:
    """Small adapter for Ollama's OpenAI-compatible chat-completions endpoint."""

    def __init__(self, base_url: str, model: str, timeout_seconds: float = 60) -> None:
        self.url = f"{base_url.rstrip('/')}/chat/completions"
        self.model = model
        self.timeout_seconds = timeout_seconds

    def chat(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "stream": False,
        }
        try:
            response = httpx.post(self.url, json=payload, timeout=self.timeout_seconds)
            response.raise_for_status()
            data = response.json()
        except httpx.TimeoutException as exc:
            raise RuntimeError("LLM request timed out") from exc
        except httpx.HTTPError as exc:
            raise RuntimeError(f"LLM request failed: {exc}") from exc
        except ValueError as exc:
            raise RuntimeError("LLM returned invalid JSON") from exc

        if not isinstance(data, dict) or not data.get("choices"):
            raise RuntimeError("LLM response did not contain choices")
        return data

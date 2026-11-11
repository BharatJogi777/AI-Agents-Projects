from typing import Any

import httpx


class OllamaClient:
    """Ollama native /api/chat adapter with JSON Schema constrained output."""

    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: float = 60,
        http_client: httpx.Client | None = None,
    ) -> None:
        normalized = base_url.rstrip("/")
        if not normalized.startswith(("http://", "https://")):
            raise ValueError("base_url must be an HTTP(S) URL")
        if not model.strip():
            raise ValueError("model cannot be empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")

        self.url = f"{normalized}/api/chat"
        self.model = model
        self.timeout = httpx.Timeout(timeout_seconds, connect=min(10.0, timeout_seconds))
        self._owns_client = http_client is None
        self._http = http_client or httpx.Client(timeout=self.timeout)

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
            response = self._http.post(self.url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except httpx.TimeoutException as exc:
            raise RuntimeError("Ollama request timed out") from exc
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Ollama returned HTTP {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            raise RuntimeError("Ollama connection failed") from exc
        except ValueError as exc:
            raise RuntimeError("Ollama returned invalid JSON") from exc

        if not isinstance(data, dict):
            raise RuntimeError("Ollama response must be a JSON object")
        message = data.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Ollama response did not contain non-empty message.content")
        return content

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

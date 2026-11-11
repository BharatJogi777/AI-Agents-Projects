"""Ollama provider adapter with pooled HTTP connections and bounded timeouts."""

from typing import Any

import httpx


class OllamaClient:
    def __init__(
        self,
        model: str = "qwen3:4b",
        base_url: str = "http://localhost:11434",
        timeout_seconds: float = 60,
        http_client: httpx.Client | None = None,
    ) -> None:
        base = base_url.rstrip("/")
        if not base.startswith(("http://", "https://")):
            raise ValueError("base_url must be an HTTP(S) URL")
        if not model.strip():
            raise ValueError("model cannot be empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.url = f"{base}/api/chat"
        self.model = model
        self.timeout = httpx.Timeout(timeout_seconds, connect=min(10.0, timeout_seconds))
        self._owns_client = http_client is None
        self._http = http_client or httpx.Client(timeout=self.timeout)

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> dict[str, Any]:
        try:
            response = self._http.post(
                self.url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "tools": tools,
                    "stream": False,
                },
                timeout=self.timeout,
            )
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

        if not isinstance(data, dict) or not isinstance(data.get("message"), dict):
            raise RuntimeError("Ollama returned an invalid chat response")
        return data

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

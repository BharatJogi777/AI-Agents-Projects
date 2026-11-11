from typing import Any

import httpx


class OllamaChatClient:
    """Reusable HTTP adapter for Ollama's OpenAI-compatible API.

    One httpx.Client is retained so repeated agent steps reuse TCP connections.
    Tests can inject a MockTransport-backed client without starting Ollama.
    """

    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: float = 60,
        http_client: httpx.Client | None = None,
    ) -> None:
        normalized = base_url.rstrip("/")
        if not normalized:
            raise ValueError("base_url cannot be empty")
        if not model.strip():
            raise ValueError("model cannot be empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")

        self.base_url = normalized
        self.url = f"{normalized}/chat/completions"
        self.model = model
        self.timeout = httpx.Timeout(timeout_seconds, connect=min(10.0, timeout_seconds))
        self._owns_client = http_client is None
        self._http = http_client or httpx.Client(timeout=self.timeout)

    def chat(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "stream": False,
        }
        try:
            response = self._http.post(self.url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except httpx.TimeoutException as exc:
            raise RuntimeError("LLM request timed out") from exc
        except httpx.HTTPStatusError as exc:
            # Do not leak provider response bodies, which may contain sensitive data.
            raise RuntimeError(f"LLM provider returned HTTP {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            raise RuntimeError("LLM provider connection failed") from exc
        except ValueError as exc:
            raise RuntimeError("LLM returned invalid JSON") from exc

        if not isinstance(data, dict) or not isinstance(data.get("choices"), list) or not data["choices"]:
            raise RuntimeError("LLM response did not contain choices")
        return data

    def is_ready(self) -> bool:
        """Check that Ollama is reachable and the configured model is available."""
        root_url = self.base_url.removesuffix("/v1")
        try:
            response = self._http.get(f"{root_url}/api/tags", timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError):
            return False
        models = payload.get("models", []) if isinstance(payload, dict) else []
        return any(
            isinstance(item, dict)
            and (item.get("name") == self.model or item.get("model") == self.model)
            for item in models
        )

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

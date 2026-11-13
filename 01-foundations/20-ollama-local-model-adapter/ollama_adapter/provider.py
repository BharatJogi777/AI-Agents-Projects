"""Resilient synchronous adapter for the Ollama non-streaming chat API."""
from __future__ import annotations
import json
import math
from collections.abc import Iterator
from typing import Any
from urllib.parse import urlsplit
import httpx
from contracts import ChatRequest, ChatResponse

class OllamaProviderError(RuntimeError):
    """Base class for sanitized adapter failures."""
class OllamaUnavailable(OllamaProviderError): pass
class OllamaTimeout(OllamaProviderError): pass
class OllamaAuthenticationError(OllamaProviderError): pass
class OllamaInvalidRequest(OllamaProviderError): pass
class OllamaResponseError(OllamaProviderError): pass
class OllamaRateLimited(OllamaProviderError):
    def __init__(self, message: str, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after

class OllamaProvider:
    """Reusable pooled HTTP client; injected clients remain caller-owned."""
    def __init__(self, base_url: str = "http://localhost:11434", timeout_seconds: float = 60.0,
                 max_response_bytes: int = 8 * 1024 * 1024,
                 transport: httpx.BaseTransport | None = None,
                 http_client: httpx.Client | None = None) -> None:
        self.base_url = self._validate_url(base_url)
        if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)):
            raise TypeError("timeout_seconds must be numeric")
        if not math.isfinite(timeout_seconds) or not 0 < timeout_seconds <= 600:
            raise ValueError("timeout_seconds must be finite and in (0, 600]")
        if type(max_response_bytes) is not int or not 1024 <= max_response_bytes <= 64 * 1024 * 1024:
            raise ValueError("max_response_bytes must be between 1 KiB and 64 MiB")
        if transport is not None and http_client is not None:
            raise ValueError("provide transport or http_client, not both")
        if http_client is not None and not isinstance(http_client, httpx.Client):
            raise TypeError("http_client must be an httpx.Client")
        self.timeout_seconds = float(timeout_seconds)
        self.max_response_bytes = max_response_bytes
        self._owns_client = http_client is None
        self._closed = False
        self._client = http_client or httpx.Client(
            base_url=self.base_url, timeout=httpx.Timeout(self.timeout_seconds),
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10), transport=transport)

    @staticmethod
    def _validate_url(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("base_url is required")
        parsed = urlsplit(value.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
            raise ValueError("base_url must be a server root without credentials, query, fragment, or path")
        try:
            _ = parsed.port
        except ValueError as exc:
            raise ValueError("base_url contains an invalid port") from exc
        return value.strip().rstrip("/")

    def close(self) -> None:
        if not self._closed and self._owns_client:
            self._client.close()
        self._closed = True

    def __enter__(self) -> "OllamaProvider":
        self._ensure_open()
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("provider is closed")

    @staticmethod
    def _retry_after(response: httpx.Response) -> float | None:
        value = response.headers.get("Retry-After")
        try:
            result = float(value) if value is not None else None
        except ValueError:
            return None
        return result if result is not None and math.isfinite(result) and result >= 0 else None

    @staticmethod
    def _check_status(response: httpx.Response, operation: str) -> None:
        status = response.status_code
        if 200 <= status < 300:
            return
        # Never include response bodies; they may contain prompts or secrets.
        if status in {401, 403}:
            raise OllamaAuthenticationError(f"Ollama {operation} was not authorized")
        if status == 429:
            raise OllamaRateLimited(f"Ollama {operation} was rate limited", OllamaProvider._retry_after(response))
        if status in {400, 404, 405, 413, 422}:
            raise OllamaInvalidRequest(f"Ollama rejected {operation} (HTTP {status})")
        if status >= 500:
            raise OllamaUnavailable(f"Ollama {operation} failed (HTTP {status})")
        raise OllamaProviderError(f"Ollama {operation} failed (HTTP {status})")

    def _read_bounded(self, chunks: Iterator[bytes], operation: str) -> bytes:
        body = bytearray()
        for chunk in chunks:
            if len(body) + len(chunk) > self.max_response_bytes:
                raise OllamaResponseError(f"Ollama {operation} response exceeded configured size limit")
            body.extend(chunk)
        return bytes(body)

    def _request_json(self, method: str, path: str, operation: str, **kwargs: Any) -> dict[str, Any]:
        self._ensure_open()
        try:
            with self._client.stream(method, path, **kwargs) as response:
                self._check_status(response, operation)
                raw = self._read_bounded(response.iter_bytes(), operation)
        except httpx.TimeoutException as exc:
            raise OllamaTimeout(f"Ollama {operation} timed out") from exc
        except httpx.HTTPError as exc:
            raise OllamaUnavailable(f"Ollama {operation} could not be completed") from exc
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise OllamaResponseError(f"Ollama {operation} returned invalid JSON") from exc
        if not isinstance(payload, dict):
            raise OllamaResponseError(f"Ollama {operation} returned an unexpected JSON shape")
        return payload

    def health(self) -> bool:
        payload = self._request_json("GET", "/api/tags", "health check")
        if not isinstance(payload.get("models"), list):
            raise OllamaResponseError("Ollama returned an invalid model list")
        return True

    def list_models(self) -> list[dict[str, Any]]:
        payload = self._request_json("GET", "/api/tags", "model listing")
        models = payload.get("models")
        if not isinstance(models, list) or any(not isinstance(item, dict) for item in models):
            raise OllamaResponseError("Ollama returned an invalid model list")
        return models

    def chat(self, request: ChatRequest) -> ChatResponse:
        if not isinstance(request, ChatRequest):
            raise TypeError("request must be a ChatRequest")
        body = {"model": request.model,
                "messages": [{"role": m.role, "content": m.content} for m in request.messages],
                "stream": False,
                "options": {"temperature": request.temperature, "num_predict": request.max_tokens}}
        payload = self._request_json("POST", "/api/chat", "chat", json=body)
        message = payload.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("content"), str):
            raise OllamaResponseError("Ollama returned an invalid chat message")
        model = payload.get("model", request.model)
        if not isinstance(model, str) or not model.strip():
            raise OllamaResponseError("Ollama returned an invalid model name")
        done = payload.get("done")
        if done is not None and not isinstance(done, bool):
            raise OllamaResponseError("Ollama returned an invalid completion flag")
        usage: dict[str, int] = {}
        for source, target in (("prompt_eval_count", "input_tokens"), ("eval_count", "output_tokens")):
            value = payload.get(source)
            if value is not None:
                if type(value) is not int or value < 0:
                    raise OllamaResponseError("Ollama returned invalid token usage")
                usage[target] = value
        reason = payload.get("done_reason")
        if reason is not None and not isinstance(reason, str):
            raise OllamaResponseError("Ollama returned an invalid finish reason")
        return ChatResponse(content=message["content"], model=model,
                            finish_reason=reason or ("stop" if done is True else None),
                            usage=usage, raw={"done": done, **({"done_reason": reason} if reason else {})})
"""HTTPX adapter for OpenAI-compatible /chat/completions endpoints."""
from __future__ import annotations
import json
import math
from collections.abc import Iterator
from typing import Any
from urllib.parse import urlsplit
import httpx
from .contracts import Request, Response

class ProviderError(RuntimeError):
    """Base class for sanitized provider adapter failures."""
class ProviderUnavailable(ProviderError): pass
class ProviderTimeout(ProviderError): pass
class ProviderAuthenticationError(ProviderError): pass
class ProviderInvalidRequest(ProviderError): pass
class ProviderResponseError(ProviderError): pass
class ProviderRateLimited(ProviderError):
    def __init__(self, message: str, retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after

class OpenAICompatibleProvider:
    """Reusable pooled HTTP client for non-streaming chat completions.

    The base URL is the API root, often ending in /v1. Internally created
    clients are owned by this instance; injected clients remain caller-owned.
    """
    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 60,
                 max_response_bytes: int = 8 * 1024 * 1024,
                 transport: httpx.BaseTransport | None = None,
                 http_client: httpx.Client | None = None) -> None:
        self.base_url = self._validate_url(base_url)
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
            raise TypeError("timeout must be numeric")
        if not math.isfinite(timeout) or not 0 < timeout <= 600:
            raise ValueError("timeout must be finite and in (0, 600]")
        if type(max_response_bytes) is not int or not 1024 <= max_response_bytes <= 64 * 1024 * 1024:
            raise ValueError("max_response_bytes must be between 1 KiB and 64 MiB")
        if api_key is not None and (not isinstance(api_key, str) or not api_key.strip()
                                    or "\r" in api_key or "\n" in api_key):
            raise ValueError("api_key must be a non-empty single-line string when provided")
        if transport is not None and http_client is not None:
            raise ValueError("provide transport or http_client, not both")
        if http_client is not None and not isinstance(http_client, httpx.Client):
            raise TypeError("http_client must be an httpx.Client")
        self.api_key = api_key.strip() if api_key else None
        self.max_response_bytes = max_response_bytes
        self._owns_client = http_client is None
        self._closed = False
        self._client = http_client or httpx.Client(
            base_url=self.base_url.rstrip("/") + "/",
            timeout=httpx.Timeout(float(timeout)),
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
            transport=transport,
        )

    @staticmethod
    def _validate_url(value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("base_url is required")
        parsed = urlsplit(value.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("base_url must not contain credentials, query, or fragment")
        if parsed.path and not parsed.path.startswith("/"):
            raise ValueError("base_url contains an invalid API path")
        try:
            _ = parsed.port
        except ValueError as exc:
            raise ValueError("base_url contains an invalid port") from exc
        return value.strip().rstrip("/")

    def close(self) -> None:
        if not self._closed and self._owns_client:
            self._client.close()
        self._closed = True

    def __enter__(self) -> "OpenAICompatibleProvider":
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
            delay = float(value) if value is not None else None
        except ValueError:
            return None
        return delay if delay is not None and math.isfinite(delay) and delay >= 0 else None

    @staticmethod
    def _check_status(response: httpx.Response) -> None:
        status = response.status_code
        if 200 <= status < 300:
            return
        # Do not expose response bodies; they may contain request data or secrets.
        if status in {401, 403}:
            raise ProviderAuthenticationError("provider rejected API authentication")
        if status == 429:
            raise ProviderRateLimited("provider rate limit exceeded",
                                      OpenAICompatibleProvider._retry_after(response))
        if status in {400, 404, 405, 413, 422}:
            raise ProviderInvalidRequest(f"provider rejected the request (HTTP {status})")
        if status >= 500:
            raise ProviderUnavailable(f"provider returned HTTP {status}")
        raise ProviderError(f"provider request failed (HTTP {status})")

    def _read_bounded(self, chunks: Iterator[bytes]) -> bytes:
        body = bytearray()
        for chunk in chunks:
            if len(body) + len(chunk) > self.max_response_bytes:
                raise ProviderResponseError("provider response exceeded configured size limit")
            body.extend(chunk)
        return bytes(body)

    def _request_json(self, body: dict[str, Any]) -> dict[str, Any]:
        self._ensure_open()
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        try:
            with self._client.stream("POST", "chat/completions", headers=headers, json=body) as response:
                self._check_status(response)
                raw = self._read_bounded(response.iter_bytes())
        except httpx.TimeoutException as exc:
            raise ProviderTimeout("chat completion request timed out") from exc
        except httpx.HTTPError as exc:
            raise ProviderUnavailable("chat completion request could not be completed") from exc
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ProviderResponseError("provider returned invalid JSON") from exc
        if not isinstance(payload, dict):
            raise ProviderResponseError("provider returned an unexpected JSON shape")
        return payload

    def chat(self, request: Request) -> Response:
        if not isinstance(request, Request):
            raise TypeError("request must be a Request")
        body = {
            "model": request.model,
            "messages": [{"role": message.role, "content": message.content} for message in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": False,
        }
        payload = self._request_json(body)
        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
            raise ProviderResponseError("provider returned an invalid choices collection")
        choice = choices[0]
        message = choice.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("content"), str):
            raise ProviderResponseError("provider returned invalid assistant content")
        model = payload.get("model", request.model)
        if not isinstance(model, str) or not model.strip():
            raise ProviderResponseError("provider returned an invalid model name")
        reason = choice.get("finish_reason")
        if reason is not None and not isinstance(reason, str):
            raise ProviderResponseError("provider returned an invalid finish reason")
        raw_usage = payload.get("usage")
        if raw_usage is None:
            raw_usage = {}
        if not isinstance(raw_usage, dict):
            raise ProviderResponseError("provider returned invalid usage metadata")
        usage: dict[str, int] = {}
        for source, target in (("prompt_tokens", "input_tokens"),
                               ("completion_tokens", "output_tokens")):
            value = raw_usage.get(source)
            if value is not None:
                if type(value) is not int or value < 0:
                    raise ProviderResponseError("provider returned invalid token usage")
                usage[target] = value
        return Response(message["content"], model, reason, usage)

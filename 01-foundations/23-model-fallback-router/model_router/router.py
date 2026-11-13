"""Bounded, deterministic multi-provider model fallback routing."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
from typing import Callable, Protocol
from registry import CapabilityRegistry, ModelCapabilities
from .errors import FallbackBudgetExceeded, NoModelAvailable, ProviderCallError

class ChatProvider(Protocol):
    """Minimal adapter contract. Implementations should enforce their own I/O timeout."""
    def chat(self, model_id: str, prompt: str) -> str: ...

@dataclass(frozen=True, slots=True)
class AttemptRecord:
    provider: str
    canonical_model_id: str
    provider_model_id: str
    outcome: str
    duration_seconds: float
    error_type: str | None = None

@dataclass(frozen=True, slots=True)
class RouteResult:
    model_id: str
    response: str
    attempts: tuple[str, ...]
    provider: str = ""
    provider_model_id: str = ""
    attempt_records: tuple[AttemptRecord, ...] = ()
    duration_seconds: float = 0.0

@dataclass(frozen=True, slots=True)
class RouteRequest:
    prompt: str
    provider_order: tuple[str, ...] = ()
    tools: bool = False
    json_schema: bool = False
    streaming: bool = False
    vision: bool = False
    min_context: int = 1
    min_output: int = 1
    max_attempts: int = 3

    def __post_init__(self):
        if not isinstance(self.prompt, str) or not self.prompt.strip():
            raise ValueError("prompt cannot be empty")
        if not isinstance(self.provider_order, tuple):
            raise TypeError("provider_order must be a tuple")
        if any(not isinstance(p, str) or not p.strip() for p in self.provider_order):
            raise ValueError("provider_order must contain non-empty provider names")
        if len(set(self.provider_order)) != len(self.provider_order):
            raise ValueError("provider_order must not contain duplicates")
        for name in ("tools", "json_schema", "streaming", "vision"):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be boolean")
        for name, value in (("min_context", self.min_context), ("min_output", self.min_output),
                            ("max_attempts", self.max_attempts)):
            if type(value) is not int or value < 1:
                raise ValueError(f"{name} must be a positive integer")

class ModelFallbackRouter:
    """Try a finite set of compatible routes, never retrying the same pair."""
    def __init__(self, registry: CapabilityRegistry, providers: dict[str, ChatProvider],
                 is_healthy: Callable[[str], bool] | None = None, *,
                 max_attempts: int = 3, clock: Callable[[], float] = monotonic,
                 retry_classifier: Callable[[Exception], bool] | None = None):
        if not isinstance(registry, CapabilityRegistry):
            raise TypeError("registry must be CapabilityRegistry")
        if not isinstance(providers, dict) or any(not isinstance(n, str) or not n.strip() for n in providers):
            raise TypeError("providers must map non-empty names to provider adapters")
        if type(max_attempts) is not int or max_attempts < 1:
            raise ValueError("max_attempts must be a positive integer")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self.registry, self.providers = registry, dict(providers)
        self.is_healthy = is_healthy or (lambda _provider: True)
        self.max_attempts, self.clock = max_attempts, clock
        self.retry_classifier = retry_classifier or (lambda _exc: True)

    def _candidate_routes(self, request: RouteRequest):
        models = self.registry.select(
            tools=request.tools, json_schema=request.json_schema,
            streaming=request.streaming, vision=request.vision,
            min_context=request.min_context, min_output=request.min_output,
        )
        rank = {name: i for i, name in enumerate(request.provider_order)}
        routes = [(model, provider) for model in models for provider in model.providers
                  if (not request.provider_order or provider in rank) and provider in self.providers]
        routes.sort(key=lambda route: (
            rank.get(route[1], len(rank)), -route[0].context_tokens,
            -route[0].max_output_tokens, route[0].model_id, route[1],
        ))
        return routes

    def generate_request(self, request: RouteRequest) -> RouteResult:
        if not isinstance(request, RouteRequest):
            raise TypeError("request must be RouteRequest")
        started = self.clock()
        routes = self._candidate_routes(request)
        if not routes:
            raise NoModelAvailable("no registered model satisfies the requested capabilities")
        attempts, records = [], []
        limit = min(request.max_attempts, self.max_attempts)
        for model, provider_name in routes:
            if len(attempts) >= limit:
                raise FallbackBudgetExceeded(
                    f"fallback attempt budget ({limit}) exhausted", attempts=tuple(attempts))
            try:
                healthy = self.is_healthy(provider_name)
            except Exception:
                # Fail closed: don't send traffic if readiness cannot be established.
                continue
            if not healthy:
                continue
            provider_model_id = model.provider_model_id(provider_name)
            attempts.append(f"{provider_name}:{model.model_id}")
            attempt_started = self.clock()
            try:
                response = self.providers[provider_name].chat(provider_model_id, request.prompt)
                if not isinstance(response, str) or not response.strip():
                    raise ProviderCallError("provider returned an empty or non-text response")
                records.append(AttemptRecord(provider_name, model.model_id, provider_model_id,
                    "success", max(0.0, self.clock() - attempt_started)))
                return RouteResult(model_id=model.model_id, response=response, attempts=tuple(attempts),
                    provider=provider_name, provider_model_id=provider_model_id,
                    attempt_records=tuple(records), duration_seconds=max(0.0, self.clock() - started))
            except Exception as exc:
                records.append(AttemptRecord(provider_name, model.model_id, provider_model_id,
                    "failed", max(0.0, self.clock() - attempt_started), type(exc).__name__))
                if isinstance(exc, ProviderCallError) and not exc.fallback_allowed:
                    raise NoModelAvailable("provider rejected the request; fallback is disabled",
                        attempts=tuple(attempts)) from None
                if not isinstance(exc, ProviderCallError) and not self.retry_classifier(exc):
                    raise NoModelAvailable("provider failure is classified as non-retryable",
                        attempts=tuple(attempts)) from None
        raise NoModelAvailable(
            f"no compatible model succeeded after {len(attempts)} provider attempt(s)",
            attempts=tuple(attempts))

    def generate(self, prompt: str, *, provider_order: tuple[str, ...] = (),
                 tools: bool = False, json_schema: bool = False, streaming: bool = False,
                 vision: bool = False, min_context: int = 1, min_output: int = 1,
                 max_attempts: int | None = None) -> RouteResult:
        return self.generate_request(RouteRequest(
            prompt=prompt, provider_order=provider_order, tools=tools,
            json_schema=json_schema, streaming=streaming, vision=vision,
            min_context=min_context, min_output=min_output,
            max_attempts=self.max_attempts if max_attempts is None else max_attempts,
        ))

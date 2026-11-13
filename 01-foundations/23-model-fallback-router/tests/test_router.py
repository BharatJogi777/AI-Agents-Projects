import pytest
from app import (CapabilityRegistry, FallbackBudgetExceeded, ModelCapabilities,
    ModelFallbackRouter, NoModelAvailable, ProviderCallError, RouteRequest)

class Provider:
    def __init__(self, result=None, error=None):
        self.result, self.error, self.calls = result, error, []
    def chat(self, model, prompt):
        self.calls.append((model, prompt))
        if self.error: raise self.error
        return self.result

def setup():
    registry = CapabilityRegistry()
    registry.register(ModelCapabilities("first", ("p1",), 8000, 1000))
    registry.register(ModelCapabilities("second", ("p2",), 4000, 1000))
    return registry

def test_fallback_after_provider_failure():
    p1, p2 = Provider(error=ConnectionError()), Provider("answer")
    result = ModelFallbackRouter(setup(), {"p1": p1, "p2": p2}).generate("question")
    assert (result.model_id, result.provider, result.response) == ("second", "p2", "answer")
    assert result.attempts == ("p1:first", "p2:second")
    assert [r.outcome for r in result.attempt_records] == ["failed", "success"]

def test_preferred_provider_beats_larger_context():
    registry = CapabilityRegistry()
    registry.register(ModelCapabilities("big", ("p1",), 64000, 4000))
    registry.register(ModelCapabilities("preferred", ("p2",), 8000, 2000))
    result = ModelFallbackRouter(registry, {"p1": Provider("one"), "p2": Provider("two")}).generate(
        "x", provider_order=("p2", "p1"))
    assert result.provider == "p2"

def test_capability_filters_and_provider_specific_id():
    registry = CapabilityRegistry()
    registry.register(ModelCapabilities("tool", ("p2",), 10000, 2000, supports_tools=True,
        provider_model_ids={"p2": "tenant/tool-model"}))
    provider = Provider("ok")
    result = ModelFallbackRouter(registry, {"p2": provider}).generate(
        "x", tools=True, min_context=9000)
    assert result.provider_model_id == "tenant/tool-model"
    assert provider.calls == [("tenant/tool-model", "x")]

def test_missing_provider_and_unhealthy_provider_are_skipped():
    registry = setup()
    p2 = Provider("ok")
    router = ModelFallbackRouter(registry, {"p2": p2}, is_healthy=lambda name: name != "p1")
    result = router.generate("x")
    assert result.attempts == ("p2:second",)

def test_health_check_exception_fails_closed():
    p1 = Provider("one")
    router = ModelFallbackRouter(setup(), {"p1": p1, "p2": Provider("two")},
        is_healthy=lambda _name: (_ for _ in ()).throw(RuntimeError()))
    with pytest.raises(NoModelAvailable):
        router.generate("x")
    assert not p1.calls

def test_empty_response_triggers_fallback():
    result = ModelFallbackRouter(setup(), {"p1": Provider("  "), "p2": Provider("valid")}).generate("x")
    assert result.provider == "p2"

def test_max_attempts_is_bounded():
    router = ModelFallbackRouter(setup(), {"p1": Provider(error=TimeoutError()),
        "p2": Provider("answer")}, max_attempts=1)
    with pytest.raises(FallbackBudgetExceeded) as error:
        router.generate("x")
    assert error.value.attempts == ("p1:first",)

def test_request_wide_failure_can_disable_fallback():
    router = ModelFallbackRouter(setup(), {"p1": Provider(error=ProviderCallError(
        "invalid payload", fallback_allowed=False)), "p2": Provider("should-not-run")})
    with pytest.raises(NoModelAvailable, match="fallback is disabled"):
        router.generate("x")

def test_non_retryable_exception_classifier_stops():
    router = ModelFallbackRouter(setup(), {"p1": Provider(error=ValueError()),
        "p2": Provider("should-not-run")}, retry_classifier=lambda exc: not isinstance(exc, ValueError))
    with pytest.raises(NoModelAvailable, match="non-retryable"):
        router.generate("x")

def test_invalid_inputs_and_duplicate_preferences():
    router = ModelFallbackRouter(setup(), {"p1": Provider("ok")})
    with pytest.raises(ValueError): router.generate(" ")
    with pytest.raises(ValueError): RouteRequest("x", provider_order=("p1", "p1"))
    with pytest.raises(ValueError): RouteRequest("x", max_attempts=0)

def test_no_compatible_model():
    with pytest.raises(NoModelAvailable):
        ModelFallbackRouter(setup(), {"p1": Provider("ok")}).generate("x", tools=True)

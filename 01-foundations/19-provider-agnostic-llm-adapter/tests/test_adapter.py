import pytest

from app import (
    ChatMessage, ChatRequest, ChatResponse, LLMClient,
    ProviderAuthenticationError, ProviderContractError, ProviderNotRegistered,
    ProviderRateLimited,
)


class FakeProvider:
    def __init__(self, response=None):
        self.last = None
        self.response = response or ChatResponse("hello", "fake-model", "stop", {"input_tokens": 2})

    def chat(self, request):
        self.last = request
        return self.response


def request(**kwargs):
    return ChatRequest((ChatMessage("user", "Hi"),), "local-model", **kwargs)


def test_default_and_explicit_provider_routing():
    first, second = FakeProvider(), FakeProvider()
    client = LLMClient({"first": first, "second": second}, "first")
    assert client.chat(request()).content == "hello"
    assert first.last is not None and second.last is None
    client.chat(request(), "second")
    assert second.last is not None


def test_unknown_provider_is_rejected_without_fallback():
    with pytest.raises(ProviderNotRegistered):
        LLMClient({"first": FakeProvider()}, "first").chat(request(), "missing")


def test_provider_registry_is_defensively_copied():
    providers = {"first": FakeProvider()}
    client = LLMClient(providers, "first")
    providers.clear()
    assert client.provider_names == ("first",)


def test_adapter_must_return_normalized_response():
    class BadProvider:
        def chat(self, req):
            return {"content": "not normalized"}
    with pytest.raises(ProviderContractError):
        LLMClient({"bad": BadProvider()}, "bad").chat(request())


@pytest.mark.parametrize("messages,model,kwargs", [
    ((), "model", {}),
    ((ChatMessage("user", "x"),), "", {}),
    ((ChatMessage("unknown", "x"),), "model", {}),
    ((ChatMessage("user", "x"),), "model", {"temperature": 3}),
    ((ChatMessage("user", "x"),), "model", {"temperature": float("nan")}),
    ((ChatMessage("user", "x"),), "model", {"max_tokens": True}),
    ((ChatMessage("user", "x"),), "model", {"max_tokens": 0}),
])
def test_request_validation(messages, model, kwargs):
    with pytest.raises((ValueError, TypeError)):
        ChatRequest(messages, model, **kwargs)


def test_metadata_is_json_validated_and_detached():
    metadata = {"trace": {"tags": ["a"]}}
    req = request(metadata=metadata)
    metadata["trace"]["tags"].append("mutated")
    assert req.metadata["trace"]["tags"] == ("a",)
    with pytest.raises(TypeError):
        req.metadata["trace"]["new"] = "value"
    with pytest.raises(AttributeError):
        req.metadata["trace"]["tags"].append("blocked")
    with pytest.raises(TypeError):
        req.metadata["new"] = "value"
    with pytest.raises(ValueError):
        request(metadata={"bad": object()})


def test_response_usage_validation_and_raw_detachment():
    raw = {"provider": {"id": "abc"}}
    response = ChatResponse("ok", "model", usage={"input_tokens": 3}, raw=raw)
    raw["provider"]["id"] = "changed"
    assert response.raw["provider"]["id"] == "abc"
    with pytest.raises(ValueError):
        ChatResponse("ok", "model", usage={"input_tokens": -1})


def test_normalized_provider_errors_expose_retry_policy_metadata():
    error = ProviderRateLimited("slow down", provider="vendor", retry_after=2.5)
    assert error.retryable is True
    assert error.status_code == 429
    assert error.retry_after == 2.5
    auth = ProviderAuthenticationError("invalid credentials", provider="vendor")
    assert auth.retryable is False

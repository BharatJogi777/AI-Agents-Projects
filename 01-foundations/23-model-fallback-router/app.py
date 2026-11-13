"""Public facade and runnable no-network demonstration."""
from model_router import (AttemptRecord, ChatProvider, FallbackBudgetExceeded, ModelFallbackRouter,
    ModelRoutingError, NoModelAvailable, ProviderCallError, RouteRequest, RouteResult)
from registry import CapabilityRegistry, ModelCapabilities

__all__ = ["AttemptRecord", "CapabilityRegistry", "ChatProvider", "FallbackBudgetExceeded",
    "ModelCapabilities", "ModelFallbackRouter", "ModelRoutingError", "NoModelAvailable",
    "ProviderCallError", "RouteRequest", "RouteResult"]

def build_demo_router():
    class DemoProvider:
        def __init__(self, answer): self.answer = answer
        def chat(self, model_id: str, prompt: str) -> str:
            return f"[{model_id}] {self.answer}: {prompt}"
    registry = CapabilityRegistry()
    registry.register(ModelCapabilities("local-small", ("ollama",), 8192, 2048,
        provider_model_ids={"ollama": "qwen3:4b"}))
    registry.register(ModelCapabilities("cloud-backup", ("openai-compatible",), 32768, 4096,
        provider_model_ids={"openai-compatible": "example/chat-model"}))
    return ModelFallbackRouter(registry, {
        "ollama": DemoProvider("local demo response"),
        "openai-compatible": DemoProvider("backup demo response"),
    })

if __name__ == "__main__":
    result = build_demo_router().generate("Explain why fallback routing is useful.")
    print(f"provider={result.provider}, model={result.model_id}")
    print(result.response)

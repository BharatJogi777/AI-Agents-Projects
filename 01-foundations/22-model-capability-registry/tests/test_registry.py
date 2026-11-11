import pytest
from app import CapabilityRegistry,ModelCapabilities

def model(name,**kw): return ModelCapabilities(name,("ollama",),8192,2048,**kw)
def test_register_and_filter():
    r=CapabilityRegistry(); r.register(model("basic")); r.register(model("tool",supports_tools=True,supports_streaming=True))
    r.register(ModelCapabilities("vision",("cloud",),32000,4000,supports_vision=True))
    assert [m.model_id for m in r.select(tools=True)]==["tool"]
    assert [m.model_id for m in r.select(provider="cloud",vision=True)]==["vision"]
def test_sorted_by_context_then_name():
    r=CapabilityRegistry(); r.register(model("z")); r.register(ModelCapabilities("large",("ollama",),32000,4096)); r.register(model("a"))
    assert [m.model_id for m in r.select()]==["large","a","z"]
def test_duplicate_unknown_and_limits():
    r=CapabilityRegistry(); r.register(model("x"))
    with pytest.raises(ValueError): r.register(model("x"))
    with pytest.raises(KeyError): r.get("missing")
    with pytest.raises(ValueError): ModelCapabilities("bad",("p",),100,200)

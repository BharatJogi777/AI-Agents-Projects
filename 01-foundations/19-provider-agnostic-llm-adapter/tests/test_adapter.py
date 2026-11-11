import pytest
from app import ChatMessage,ChatRequest,ChatResponse,LLMClient


class FakeProvider:
    def __init__(self): self.last=None
    def chat(self,request):
        self.last=request
        return ChatResponse("hello","fake-model","stop",{"input_tokens":2})


def request():
    return ChatRequest((ChatMessage("user","Hi"),),"local-model")


def test_default_and_explicit_provider_routing():
    a,b=FakeProvider(),FakeProvider()
    client=LLMClient({"a":a,"b":b},"a")
    assert client.chat(request()).content=="hello"
    assert a.last is not None and b.last is None
    client.chat(request(),"b")
    assert b.last is not None


def test_unknown_provider_rejected():
    client=LLMClient({"a":FakeProvider()},"a")
    with pytest.raises(ValueError,match="not registered"): client.chat(request(),"c")


def test_request_validation():
    with pytest.raises(ValueError): ChatRequest((),"model")
    with pytest.raises(ValueError): ChatRequest((ChatMessage("user","x"),),"",)
    with pytest.raises(ValueError): ChatRequest((ChatMessage("user","x"),),"m",temperature=3)


def test_provider_response_contract_enforced():
    class Bad:
        def chat(self,r): return {"content":"not normalized"}
    with pytest.raises(TypeError): LLMClient({"bad":Bad()},"bad").chat(request())

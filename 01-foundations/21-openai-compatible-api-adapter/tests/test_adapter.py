import json,httpx,pytest
from app import Message,Request,OpenAICompatibleProvider,ProviderError

def req(): return Request("test-model",(Message("user","Hi"),),.1,100)
def test_mapping():
    def handler(r):
        assert r.url.path=="/v1/chat/completions" and r.headers["authorization"]=="Bearer secret"
        assert json.loads(r.content)["messages"]==[{"role":"user","content":"Hi"}]
        return httpx.Response(200,json={"model":"served","choices":[{"message":{"content":"Hello"},"finish_reason":"stop"}],"usage":{"prompt_tokens":4,"completion_tokens":2}})
    out=OpenAICompatibleProvider("https://example.test/v1","secret",transport=httpx.MockTransport(handler)).chat(req())
    assert (out.content,out.model,out.finish_reason)==("Hello","served","stop")
    assert out.usage=={"input_tokens":4,"output_tokens":2}
def test_http_and_shape_errors():
    p=OpenAICompatibleProvider("https://example.test/v1",transport=httpx.MockTransport(lambda r:httpx.Response(502)))
    with pytest.raises(ProviderError): p.chat(req())
    p=OpenAICompatibleProvider("https://example.test/v1",transport=httpx.MockTransport(lambda r:httpx.Response(200,json={"choices":[]})))
    with pytest.raises(ProviderError): p.chat(req())
def test_validation():
    with pytest.raises(ValueError): Request("",(Message("user","x"),))
    with pytest.raises(ValueError): Message("tool","x")
    with pytest.raises(ValueError): OpenAICompatibleProvider("file:///tmp")

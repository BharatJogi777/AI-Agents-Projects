import json,pytest
from app import ChatCompletionStreamParser,StreamProtocolError
def frame(x): return "data: "+json.dumps(x)+"\n\n"
def test_incremental_stream():
    p=ChatCompletionStreamParser()
    a=frame({"choices":[{"delta":{"content":"Hel"},"finish_reason":None}]})
    b=frame({"choices":[{"delta":{"content":"lo"},"finish_reason":None}]})
    c=frame({"choices":[{"delta":{},"finish_reason":"stop"}]})
    events=p.feed(a[:9])+p.feed(a[9:]+b+c)
    assert "".join(x.text for x in events)=="Hello" and events[-1].finished
def test_done_and_closed_state():
    p=ChatCompletionStreamParser(); assert p.feed("data: [DONE]\n\n")[0].finished
    with pytest.raises(StreamProtocolError): p.feed("data: [DONE]\n\n")
def test_invalid_json_and_shape():
    with pytest.raises(StreamProtocolError): ChatCompletionStreamParser().feed("data: nope\n\n")
    with pytest.raises(StreamProtocolError): ChatCompletionStreamParser().feed("data: {}\n\n")
def test_close_flushes_partial_frame():
    p=ChatCompletionStreamParser(); p.feed('data: {"choices":[{"delta":{"content":"x"}}]}')
    assert p.close()[0].text=="x"

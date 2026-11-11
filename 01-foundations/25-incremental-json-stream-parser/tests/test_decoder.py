import pytest
from app import IncrementalJSONDecoder,IncrementalJSONError
def test_fragmented_object():
    d=IncrementalJSONDecoder(); assert d.feed('{"name":')==[]
    assert d.feed('"Ada","n":2}')==[{"name":"Ada","n":2}]
    assert d.finish()==[]
def test_multiple_values():
    d=IncrementalJSONDecoder(); assert d.feed('{"a":1} [2,3] true')==[{"a":1},[2,3],True]
def test_incomplete_stream():
    d=IncrementalJSONDecoder(); d.feed('{"a":')
    with pytest.raises(IncrementalJSONError): d.finish()
def test_limits_and_type():
    with pytest.raises(IncrementalJSONError): IncrementalJSONDecoder(5).feed("123456")
    with pytest.raises(TypeError): IncrementalJSONDecoder().feed(b"{}")
def test_whitespace():
    d=IncrementalJSONDecoder(); d.feed("   "); assert d.finish()==[]

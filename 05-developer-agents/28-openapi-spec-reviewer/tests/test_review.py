import pytest
from app.openapi_review import review

def test_valid_minimal_spec():
    spec={"openapi":"3.1.0","info":{"title":"API","version":"1"},"paths":{"/x":{"get":{"responses":{"200":{"description":"ok"}},"operationId":"getX"}}}}
    assert review(spec)==[]

def test_missing_responses_and_operation_id():
    result=review({"openapi":"3.0.0","info":{"title":"A","version":"1"},"paths":{"/x":{"get":{}}}})
    assert any("responses" in f["path"] for f in result)
    assert any("operationId" in f["path"] for f in result)

def test_non_object_rejected():
    with pytest.raises(ValueError): review([])

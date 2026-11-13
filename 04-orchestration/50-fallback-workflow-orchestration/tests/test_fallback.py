import pytest
from app.fallback import execute_with_fallback

def test_fallback_to_successful_strategy():
    result=execute_with_fallback([("primary",lambda:1/0),("backup",lambda:"ok")])
    assert result.value == "ok" and result.strategy == "backup"
    assert [a.succeeded for a in result.attempts] == [False,True]

def test_all_fail_and_empty():
    with pytest.raises(RuntimeError): execute_with_fallback([("a",lambda:1/0)])
    with pytest.raises(ValueError): execute_with_fallback([])

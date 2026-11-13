import pytest
from app.deadlock import explain
def test_cycle(): assert explain({"a":["b"],"b":["a"]})[0]["cycle"]==["a","b","a"]
def test_acyclic(): assert explain({"a":["b"],"b":[]})==[]
def test_invalid():
 with pytest.raises(ValueError): explain({"a":"b"})

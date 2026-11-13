import pytest
from app.aggregator import AgentResult, aggregate

def test_filters_errors_and_low_confidence():
    a=AgentResult("a",1,.9); b=AgentResult("b",2,.4); c=AgentResult("c",3,.99,("tool failed",))
    result=aggregate([a,b,c],.5)
    assert result.accepted == (a,) and len(result.rejected) == 2

def test_duplicate_and_invalid_confidence():
    with pytest.raises(ValueError): aggregate([AgentResult("a",1,.5),AgentResult("a",2,.6)])
    with pytest.raises(ValueError): aggregate([AgentResult("a",1,1.2)])

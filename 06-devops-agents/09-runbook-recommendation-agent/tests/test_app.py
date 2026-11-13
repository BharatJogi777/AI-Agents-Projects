import pytest
from app.runbook_recommendation import Procedure, recommend_runbooks

def test_recommends_by_explicit_symptom_tags():
    p=Procedure("RB1","Check database pool",("connection saturation","timeouts"),("read pool metrics",),"high")
    result=recommend_runbooks(["timeouts"],[p])
    assert result[0]["requires_approval"] and not result[0]["execute_automatically"]

def test_rejects_empty_symptoms_and_duplicate_ids():
    with pytest.raises(ValueError): recommend_runbooks([" "],[])
    p=Procedure("x","one",("a",))
    with pytest.raises(ValueError): recommend_runbooks(["a"],[p,p])

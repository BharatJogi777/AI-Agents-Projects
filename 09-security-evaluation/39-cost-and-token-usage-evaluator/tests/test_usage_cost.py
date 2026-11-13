import pytest
from app.usage_cost import Usage, evaluate_usage

def test_cost_and_budget():
    report=evaluate_usage([Usage("a",1000,500),Usage("b",1000,500)],input_rate_per_million=1,output_rate_per_million=2,budget=.01)
    assert report.input_tokens==2000 and report.output_tokens==1000
    assert report.estimated_cost==pytest.approx(.004) and not report.over_budget

def test_negative_tokens_rejected():
    with pytest.raises(ValueError): evaluate_usage([Usage("a",-1,0)],input_rate_per_million=1,output_rate_per_million=1,budget=1)

def test_duplicate_request_ids_rejected():
    with pytest.raises(ValueError): evaluate_usage([Usage("a",1,1),Usage("a",2,2)],input_rate_per_million=1,output_rate_per_million=1,budget=1)

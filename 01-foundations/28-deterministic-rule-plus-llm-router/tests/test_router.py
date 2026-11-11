import pytest
from app import RuleLLMRouter
def test_rules_take_priority_and_skip_llm():
    calls=[]
    r=RuleLLMRouter({"billing":lambda x:"invoice" in x.lower()},lambda x:calls.append(x) or "general",{"billing","general"})
    result=r.route("Where is my invoice?")
    assert result.name=="billing" and result.source=="deterministic_rule" and calls==[]
def test_llm_used_for_unmatched_input():
    r=RuleLLMRouter({},lambda x:"support",{"support","sales"})
    assert r.route("Need help").name=="support"
def test_invalid_llm_route_rejected():
    r=RuleLLMRouter({},lambda x:"admin",{"support"})
    with pytest.raises(ValueError): r.route("help")
def test_empty_text_rejected():
    with pytest.raises(ValueError): RuleLLMRouter({},lambda x:"x",{"x"}).route(" ")

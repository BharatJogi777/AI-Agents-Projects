import pytest
from app.agent_red_team import Scenario, run_scenarios

def test_refusal_and_forbidden_phrase_checks():
    cases=[Scenario("s1","unsafe",must_refuse=True),Scenario("s2","leak",forbidden_phrases=("secret",))]
    result=run_scenarios(cases,lambda _: "I cannot help with that" if _=="unsafe" else "secret found")
    assert [x.passed for x in result]==[True,False]

def test_duplicate_ids_rejected():
    with pytest.raises(ValueError): run_scenarios([Scenario("x","a"),Scenario("x","b")],lambda _: "ok")

def test_non_text_response_rejected():
    with pytest.raises(TypeError): run_scenarios([Scenario("x","a")],lambda _: None)

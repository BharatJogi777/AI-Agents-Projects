import pytest
from app.prompt_regression import PromptCase, score_version, compare_versions

def test_scores_and_detects_new_regression():
    cases=[PromptCase("1",("hello",)),PromptCase("2",forbidden_terms=("leak",))]
    old=score_version("v1",cases,{"1":"hello","2":"safe"})
    new=score_version("v2",cases,{"1":"hello","2":"leak"})
    assert old.pass_rate==1 and compare_versions(old,new)["new_regressions"]==("2",)

def test_missing_output_rejected():
    with pytest.raises(ValueError): score_version("v1",[PromptCase("1")],{})

def test_duplicate_case_ids_rejected():
    with pytest.raises(ValueError): score_version("v1",[PromptCase("x"),PromptCase("x")],{"x":"ok"})

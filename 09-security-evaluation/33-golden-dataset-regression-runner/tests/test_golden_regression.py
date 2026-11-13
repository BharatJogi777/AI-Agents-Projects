import pytest
from app.golden_regression import run_regression

def test_all_cases_pass():
    r=run_regression([{"id":"a","expected":"yes"}],{"a":"yes"})
    assert r.pass_rate == 1 and r.passed == 1

def test_detects_regression_and_missing_output():
    r=run_regression([{"id":"a","expected":"yes"},{"id":"b","expected":"ok"}],{"a":"no"})
    assert r.failed_ids == ("a","b")

def test_duplicate_case_ids_rejected():
    with pytest.raises(ValueError): run_regression([{"id":"x","expected":"a"},{"id":"x","expected":"b"}],{})

def test_empty_dataset_is_neutral():
    assert run_regression([],{}).pass_rate == 1

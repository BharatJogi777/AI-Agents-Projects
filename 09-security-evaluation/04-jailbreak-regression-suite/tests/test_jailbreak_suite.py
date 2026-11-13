from app.jailbreak_suite import run_regression_suite

def test_reports_regression_mismatch():
    result = run_regression_suite([{"name":"safe","response":"normal","expected_safe":True},{"name":"unsafe","response":"unsafe","expected_safe":False}], lambda x: x == "normal")
    assert result["passed"] == 2 and result["failed"] == 0

def test_rejects_non_callable_validator():
    import pytest
    with pytest.raises(TypeError): run_regression_suite([], None)
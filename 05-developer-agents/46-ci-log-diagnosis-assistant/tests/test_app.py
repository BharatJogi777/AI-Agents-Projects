import pytest
from app.ci_diagnosis import diagnose_ci_log

def test_classifies_dependency_and_test_failures():
    results = diagnose_ci_log("ModuleNotFoundError: No module named 'httpx'\\nFAILED tests/test_api.py::test_get")
    assert {x.category for x in results} == {"dependency", "test"}

def test_unknown_log_is_not_misclassified():
    assert diagnose_ci_log("runner started") [0].category == "unknown"

def test_rejects_invalid_input_and_limit():
    with pytest.raises(TypeError): diagnose_ci_log(None)
    with pytest.raises(ValueError): diagnose_ci_log("x", max_chars=0)

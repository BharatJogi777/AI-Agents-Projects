import pytest
from app.testgen import generate_cases, render_pytest


def test_generates_success_and_error_templates():
    cases = generate_cases("parse", [{"input": '"12"', "expected": "12"}], ['"bad"'])
    source = render_pytest("parse", cases)
    assert "assert parse(" in source
    assert "pytest.raises" in source


def test_rejects_invalid_function_and_example_shape():
    with pytest.raises(ValueError):
        generate_cases("not-valid", [])
    with pytest.raises(ValueError):
        generate_cases("parse", [{"input": "1"}])


def test_rejects_unsafe_empty_expression():
    with pytest.raises(ValueError):
        generate_cases("parse", [{"input": "", "expected": "1"}])

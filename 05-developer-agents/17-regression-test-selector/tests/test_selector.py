import pytest
from app.selector import select_tests, to_json


def test_selects_deduplicated_tests_and_reports_unknown_impact():
    result = select_tests(["a.py", "b.py", "a.py"], {"a.py": ["test_a.py"], "b.py": ["test_a.py", "test_b.py"]})
    assert result.tests == ("test_a.py", "test_b.py")
    assert result.unmapped_files == ()
    assert '"changed_files"' in to_json(result)


def test_unmapped_files_are_explicit():
    result = select_tests(["new_module.py"], {})
    assert result.unmapped_files == ("new_module.py",)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        select_tests([""], {})
    with pytest.raises(ValueError):
        select_tests(["a.py"], {"a.py": [""]})

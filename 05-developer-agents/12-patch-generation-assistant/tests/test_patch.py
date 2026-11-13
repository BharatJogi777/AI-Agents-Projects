import pytest
from app.patch import generate_patch


def test_generates_diff_without_mutating_input():
    original = "limit = 5\n"
    patch = generate_patch(original, "", "limit = 5", "limit = 10")
    assert "--- a/source" in patch and "+limit = 10" in patch
    assert original == "limit = 5\n"


def test_missing_or_ambiguous_target_is_rejected():
    with pytest.raises(ValueError):
        generate_patch("a=1", "", "b=2", "b=3")
    with pytest.raises(ValueError):
        generate_patch("x=1\nx=1", "", "x=1", "x=2")


def test_multiple_replacements_require_opt_in():
    patch = generate_patch("x=1\nx=1", "", "x=1", "x=2", allow_multiple=True)
    assert patch.count("+x=2") == 2

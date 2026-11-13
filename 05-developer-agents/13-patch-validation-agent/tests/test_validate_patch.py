import pytest
from app.validate_patch import validate_patch, to_json


def test_detects_path_traversal_and_whitespace():
    patch = "diff --git a/a b/a\n--- a/../secret\n+++ b/a\n+bad \n"
    codes = {item.code for item in validate_patch(patch)}
    assert "unsafe-path" in codes
    assert "trailing-whitespace" in codes


def test_reports_missing_header_and_binary_patch():
    issues = validate_patch("GIT binary patch\n")
    assert {item.code for item in issues} == {"binary-change", "missing-diff-header"}
    assert '"severity"' in to_json(issues)


def test_type_validation():
    with pytest.raises(TypeError):
        validate_patch(None)

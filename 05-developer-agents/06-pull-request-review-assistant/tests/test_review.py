import pytest

from app.review import parse_added_lines, review_diff


DIFF = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1,2 +1,4 @@
 import os
+print("debug")
+verify = False
+password = "supersecretvalue"
"""


def test_parses_added_lines_with_new_line_numbers():
    assert parse_added_lines(DIFF) == [
        ("app.py", 2, 'print("debug")'),
        ("app.py", 3, "verify = False"),
        ("app.py", 4, 'password = "supersecretvalue"'),
    ]


def test_review_returns_evidence_linked_findings():
    findings = review_diff(DIFF)
    assert {item.rule_id for item in findings} == {"debug-output", "tls-disabled", "embedded-secret"}
    assert all(item.file_path == "app.py" and item.line_number for item in findings)


def test_severity_filter_and_invalid_value():
    assert all(item.severity == "high" for item in review_diff(DIFF, "high"))
    with pytest.raises(ValueError):
        review_diff(DIFF, "critical")


def test_type_validation():
    with pytest.raises(TypeError):
        parse_added_lines(None)

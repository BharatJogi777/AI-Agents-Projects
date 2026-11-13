import pytest
from app.coverage import analyze_coverage, to_json


def test_ranks_unmeasured_and_low_coverage_first():
    report = {"files": {"a.py": {"summary": {"num_statements": 10, "missing_lines": 5}},
                        "b.py": {"summary": {"num_statements": 10, "missing_lines": 0}}}}
    result = analyze_coverage(["b.py", "a.py", "c.py"], report)
    assert [x.path for x in result] == ["c.py", "a.py", "b.py"]
    assert result[1].coverage_percent == 50
    assert '"not-measured"' in to_json(result)


def test_zero_statement_file_is_fully_covered():
    result = analyze_coverage(["empty.py"], {"files": {"empty.py": {"summary": {"num_statements": 0, "missing_lines": 0}}}})
    assert result[0].coverage_percent == 100


def test_rejects_invalid_summary():
    with pytest.raises(ValueError):
        analyze_coverage(["a.py"], {"files": {"a.py": {"summary": {"num_statements": 1, "missing_lines": 2}}}})

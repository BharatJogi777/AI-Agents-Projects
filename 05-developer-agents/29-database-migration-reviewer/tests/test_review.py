import pytest
from app.migration_review import review

def test_flags_drop_and_truncate():
    result=review("DROP TABLE users;\nTRUNCATE users;")
    assert {x["severity"] for x in result}=={"critical","high"}

def test_line_numbers():
    assert review("SELECT 1;\nDROP TABLE x;")[0]["line"]==2

def test_empty_rejected():
    with pytest.raises(ValueError): review(" ")

import pytest
from app.tool_selection import evaluate_selection

def test_perfect_selection():
    assert evaluate_selection({"search"},{"search"}).f1 == 1

def test_extra_and_missing_tools():
    m=evaluate_selection({"search","delete"},{"search","read"})
    assert m.false_positives == ("delete",) and m.false_negatives == ("read",)

def test_both_empty_is_perfect():
    assert evaluate_selection(set(),set()).f1 == 1

def test_requires_sets():
    with pytest.raises(ValueError): evaluate_selection(["a"],{"a"})

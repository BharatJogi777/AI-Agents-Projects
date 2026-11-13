import pytest
from app.answer_relevance import evaluate_relevance

def test_all_topics_covered():
    r=evaluate_relevance("Explain Python async IO and memory profiling.",["Python","async IO","memory profiling"])
    assert r.score == 1.0

def test_reports_missing_topic():
    r=evaluate_relevance("Python async IO",["Python","database indexing"])
    assert r.missing_topics == ("database indexing",)

def test_case_insensitive():
    assert evaluate_relevance("PYTHON",["python"]).score == 1.0

def test_rejects_empty_topics():
    with pytest.raises(ValueError): evaluate_relevance("answer",[])

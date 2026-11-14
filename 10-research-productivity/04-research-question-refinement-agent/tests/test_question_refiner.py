import pytest
from app.question_refiner import refine_question

def test_refines_scope_and_reports_gaps():
    result = refine_question(topic="LLM evaluation", audience="backend teams", timeframe="2025-2026")
    assert "backend teams" in result.primary_question
    assert "geography" in result.missing_dimensions
    assert len(result.subquestions) == 3

def test_rejects_empty_topic_and_non_string_dimension():
    with pytest.raises(ValueError):
        refine_question(topic=" ", audience="")
    with pytest.raises(ValueError):
        refine_question(topic="AI", audience=None)

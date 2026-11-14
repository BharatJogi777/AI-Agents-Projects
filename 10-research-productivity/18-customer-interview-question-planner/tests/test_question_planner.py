import pytest
from app.question_planner import plan_questions

def test_builds_open_ended_neutral_questions():
    result=plan_questions(objectives=["Managing invoices"])
    assert len(result)==1
    assert result[0].question.startswith("Can you walk me through")
    assert "What happened next" in result[0].follow_up

def test_rejects_empty_objective():
    with pytest.raises(ValueError):
        plan_questions(objectives=[" "])

def test_rejects_non_list():
    with pytest.raises(TypeError):
        plan_questions(objectives="invoices")

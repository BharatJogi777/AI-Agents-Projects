from app.follow_up import Note, build_follow_up
import pytest

def test_missing_owner_and_due_date_are_flagged():
    result=build_follow_up([Note("Send proposal","action")])
    action=result["actions"][0]
    assert action["needs_owner_confirmation"] and action["needs_deadline_confirmation"]

def test_decisions_and_questions_are_separated():
    result=build_follow_up([Note("Approved","decision"),Note("Who owns rollout?","question")])
    assert len(result["decisions"]) == len(result["questions"]) == 1

def test_unknown_kind_rejected():
    with pytest.raises(ValueError):
        build_follow_up([Note("Text","other")])

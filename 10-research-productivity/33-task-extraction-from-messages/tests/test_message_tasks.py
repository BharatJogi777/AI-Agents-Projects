import pytest
from app.message_tasks import extract_tasks

def test_extracts_explicit_action_phrases():
    r=extract_tasks(messages=[{"id":"m1","text":"Please send the report\nThe meeting is at noon."}])
    assert len(r)==1 and r[0].task_text=="send the report"

def test_rejects_duplicate_message_ids():
    with pytest.raises(ValueError):
        extract_tasks(messages=[{"id":"x","text":"Please call"},{"id":"x","text":"Please email"}])

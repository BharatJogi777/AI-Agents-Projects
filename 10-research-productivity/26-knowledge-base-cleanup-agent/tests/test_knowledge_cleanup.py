import pytest
from app.knowledge_cleanup import plan_cleanup

def test_flags_incomplete_and_duplicate_records():
    result=plan_cleanup(records=[{"id":"a","title":"Guide","body":"Text"},{"id":"b","title":"","body":"Text"},{"id":"a","title":"Copy","body":"Text"}])
    assert [x.action for x in result] == ["keep","manual_review","manual_review"]

def test_rejects_bad_record():
    with pytest.raises(ValueError):
        plan_cleanup(records=["not a mapping"])

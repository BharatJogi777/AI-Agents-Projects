import pytest
from app.inbox_priority import prioritize_inbox

def test_ranks_deadline_and_direct_messages_first():
    result=prioritize_inbox(messages=[{"id":"a","is_unread":True},{"id":"b","is_direct":True,"has_deadline":True}])
    assert result[0].message_id=="b"
    assert result[0].score==7

def test_rejects_duplicate_message_ids():
    with pytest.raises(ValueError):
        prioritize_inbox(messages=[{"id":"x"},{"id":"x"}])

import pytest
from app.reply_drafter import draft_reply

def test_draft_requires_approval_and_is_not_sent():
    r=draft_reply(recipient="person@example.com",subject="Update",key_points=["Review the proposal"])
    assert r.requires_approval and not r.approved
    assert "Review the proposal" in r.body

def test_rejects_invalid_tone():
    with pytest.raises(ValueError):
        draft_reply(recipient="a@b.com",subject="Hi",key_points=[],tone="angry")

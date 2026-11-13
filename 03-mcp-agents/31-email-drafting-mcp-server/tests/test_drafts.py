import pytest
from app.drafts import create_draft

def test_creates_draft_without_sending():
    draft=create_draft("Incident update","We are investigating.",["ops@example.com"])
    assert draft.subject=="Incident update"
    assert draft.recipients==("ops@example.com",)

@pytest.mark.parametrize("args",[("", "body", []),("subject","",[]),("subject","body",["bad-address"]),("s","b",["a@b.com","A@B.com"])])
def test_rejects_invalid_draft(args):
    with pytest.raises(ValueError): create_draft(*args)

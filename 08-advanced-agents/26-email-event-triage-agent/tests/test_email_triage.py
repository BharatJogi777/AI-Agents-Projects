import pytest
from app.email_triage import Email, triage_emails

def test_prioritizes_security_and_promotions():
    rows=triage_emails([Email("1","a@b.com","Security breach","now"),Email("2","a@b.com","Weekly newsletter","now")])
    assert [r.priority for r in rows] == ["high","low"]
    assert all(r.action == "human_review" for r in rows)

def test_normal_default():
    assert triage_emails([Email("1","a@b.com","Hello","now")])[0].priority == "normal"

def test_rejects_duplicate_and_invalid_fields():
    e=Email("x","a@b.com","Hi","now")
    with pytest.raises(ValueError): triage_emails([e,e])
    with pytest.raises(ValueError): triage_emails([Email("y","bad","Hi","now")])

import pytest
from app.terraform_review import review_plan

def test_flags_delete_and_public_exposure():
    plan={"resource_changes":[{"address":"aws_db.main","change":{"actions":["delete","create"],"after":{"publicly_accessible":True}}}]}
    codes={x["code"] for x in review_plan(plan)}
    assert {"RESOURCE_DELETE","REPLACEMENT","PUBLIC_EXPOSURE"} <= codes

def test_rejects_missing_changes():
    with pytest.raises(ValueError): review_plan({})

from app.iam_review import review_policy
import pytest

def test_flags_wildcards_and_privilege_actions():
    result = review_policy({"Statement":{"Effect":"Allow","Action":["*","iam:CreateAccessKey"],"Resource":"*"}})
    assert len(result) == 3

def test_rejects_invalid_effect():
    with pytest.raises(ValueError): review_policy({"Statement":{"Effect":"Maybe","Action":"s3:GetObject","Resource":"*"}})

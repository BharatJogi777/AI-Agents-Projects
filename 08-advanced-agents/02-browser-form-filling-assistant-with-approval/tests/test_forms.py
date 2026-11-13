import pytest
from app.forms import FormDraft,prepare_draft,approval_token,authorize_submission
def test_exact_draft_approval():
 d=prepare_draft("https://forms.example.org",{"name":"A"},{"https://forms.example.org"})
 assert authorize_submission(d,approval_token(d))["submission_performed"] is False
def test_wrong_token_denied():
 with pytest.raises(PermissionError): authorize_submission(FormDraft("https://forms.example.org",{"name":"A"}),"wrong")
def test_unapproved_origin_denied():
 with pytest.raises(ValueError): prepare_draft("https://evil.test",{"x":"y"},set())

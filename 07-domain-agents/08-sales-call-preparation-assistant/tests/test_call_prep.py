from app.call_prep import prepare_call
import pytest

def test_builds_agenda_from_context():
    result=prepare_call(account_name="Acme",objective="Understand needs",context=["Uses legacy billing"],stakeholders=["CFO"],open_questions=["Budget?"])
    assert any("CFO" in x for x in result.agenda) and result.open_questions==("Budget?",)

def test_rejects_blank_account():
    with pytest.raises(ValueError): prepare_call(account_name="",objective="Demo",context=[],stakeholders=[],open_questions=[])

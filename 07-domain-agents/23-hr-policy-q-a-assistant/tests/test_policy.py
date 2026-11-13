import pytest
from app.policy import answer
def test_cited_retrieval():
 assert answer("parental leave",[{"id":"HR-4","text":"Parental leave eligibility"}])["matches"][0]["document_id"]=="HR-4"
def test_abstains():
 assert answer("unrelated",[{"id":"1","text":"Travel reimbursement"}])["status"]=="abstain"
def test_empty_question():
 with pytest.raises(ValueError): answer(" ",[])

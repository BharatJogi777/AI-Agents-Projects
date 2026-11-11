import pytest
from app import RetrievedEvidence,decide_answer
def test_abstains_without_evidence():
 r=decide_answer([]); assert r.abstained and r.answer is None
def test_threshold_and_source_requirement():
 e=[RetrievedEvidence("a","weak",.2),RetrievedEvidence("b","strong",.9)]; r=decide_answer(e,.5); assert not r.abstained and r.source_ids==("b",)
 assert decide_answer(e,.5,2).abstained
def test_bad_score():
 with pytest.raises(ValueError): decide_answer([RetrievedEvidence("a","x",2)])

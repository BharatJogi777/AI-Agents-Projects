import pytest
from app import HyDEAgent
def test_hypothesis_is_not_evidence():
 r=HyDEAgent(lambda q:"Possible explanation, not verified evidence.").generate("why cache stale?"); assert r.original_query=="why cache stale?" and "not verified evidence" in r.hypothetical_document
def test_bad_generator():
 with pytest.raises(ValueError): HyDEAgent(lambda q:" ").generate("question")
 with pytest.raises(ValueError): HyDEAgent(lambda q:"x"*20,10).generate("question")

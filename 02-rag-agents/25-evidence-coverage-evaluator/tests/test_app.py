import pytest
from app import ClaimEvidence,evaluate_coverage
def test_coverage():
 r=evaluate_coverage([ClaimEvidence("1","supported",("s1",)),ClaimEvidence("2","uncited",()),ClaimEvidence("3","unknown",("s2",))],{"s1"}); assert r.coverage==1/3 and r.uncovered_ids==("2","3")
def test_empty_and_duplicate_ids():
 assert evaluate_coverage([],set()).coverage==1
 with pytest.raises(ValueError): evaluate_coverage([ClaimEvidence("x","a",()),ClaimEvidence("x","b",())],set())

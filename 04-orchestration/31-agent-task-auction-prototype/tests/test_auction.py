import pytest
from app.auction import Bid, award_task

def test_lowest_eligible_bid_wins():
    bids=[Bid("a",8,5,frozenset({"search"})),Bid("b",6,7,frozenset({"search"}))]
    assert award_task("t",{"search"},bids,10,10).agent_id == "b"

def test_no_eligible_and_duplicate_bids():
    with pytest.raises(RuntimeError): award_task("t",{"x"},[],10,5)
    b=Bid("a",1,1,frozenset({"x"}))
    with pytest.raises(ValueError): award_task("t",{"x"},[b,b],10,5)

import pytest
from app.review_queue import build_review_queue

def test_priority_ordering():
    q=build_review_queue([{"item_id":"b","priority":2,"reason":"low"},{"item_id":"a","priority":5,"reason":"risk"}])
    assert [x.item_id for x in q] == ["a","b"]

def test_stable_tie_break():
    q=build_review_queue([{"item_id":"z","priority":3,"reason":"r"},{"item_id":"a","priority":3,"reason":"r"}])
    assert [x.item_id for x in q] == ["a","z"]

def test_duplicate_id_rejected():
    row={"item_id":"x","priority":1,"reason":"r"}
    with pytest.raises(ValueError): build_review_queue([row,row])

def test_invalid_priority_rejected():
    with pytest.raises(ValueError): build_review_queue([{"item_id":"x","priority":0,"reason":"r"}])

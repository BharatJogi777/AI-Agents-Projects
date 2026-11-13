from app.obligations import extract_obligations
from datetime import date
import pytest

def test_validates_and_sorts_obligations():
    result=extract_obligations([{"obligation_id":"b","description":"Send report","owner":"Ops","due_date":"2026-12-01"},{"obligation_id":"a","description":"Pay fee","owner":"Finance","due_date":"2026-11-20"}])
    assert result[0].obligation_id=="a" and result[0].due_date==date(2026,11,20)

def test_rejects_duplicate_ids():
    item={"obligation_id":"x","description":"Do task","owner":"Ops","due_date":"2026-12-01"}
    with pytest.raises(ValueError): extract_obligations([item,item])

import pytest
from app.concurrency_review import investigate
def test_classifies_and_deduplicates():
 rows=[{"kind":"shared_mutable_state","location":"cache"},{"kind":"shared_mutable_state","location":"cache"}]
 result=investigate(rows)
 assert len(result)==1 and result[0]["severity"]=="high"
def test_missing_location():
 with pytest.raises(ValueError): investigate([{"kind":"missing_timeout"}])
def test_unknown_kind():
 with pytest.raises(ValueError): investigate([{"kind":"mystery","location":"x"}])

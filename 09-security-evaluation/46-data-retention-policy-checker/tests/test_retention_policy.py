import pytest
from datetime import date
from app.retention_policy import RetentionRecord,evaluate_retention
def test_retention_and_legal_hold():
 rows=[RetentionRecord("old",date(2025,1,1)),RetentionRecord("hold",date(2025,1,1),True),RetentionRecord("new",date(2026,1,1))]
 out=evaluate_retention(rows,retention_days=30,as_of=date(2026,1,1))
 assert [x.action for x in out]==["eligible_for_deletion_review","retain","retain"]
def test_invalid_policy_and_duplicate_ids():
 with pytest.raises(ValueError): evaluate_retention([],retention_days=-1,as_of=date.today())
 with pytest.raises(ValueError): evaluate_retention([RetentionRecord("x",date(2025,1,1)),RetentionRecord("x",date(2025,1,1))],retention_days=1,as_of=date(2025,1,2))

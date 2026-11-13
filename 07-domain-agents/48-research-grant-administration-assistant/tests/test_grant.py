from datetime import date,timedelta
import pytest
from app.grant import GrantMilestone,review_milestones
def test_flags_missing_evidence_and_overdue():
 d=date(2026,1,10); m=GrantMilestone("M","G","Submit report",d-timedelta(days=1),"owner",None)
 r=review_milestones([m],d)
 assert r["attention_count"]==1 and r["milestones"][0]["evidence_missing"]
def test_rejects_duplicate_milestones():
 d=date(2026,1,1); m=GrantMilestone("M","G","Report",d,"owner","file-1")
 with pytest.raises(ValueError): review_milestones([m,m],d)

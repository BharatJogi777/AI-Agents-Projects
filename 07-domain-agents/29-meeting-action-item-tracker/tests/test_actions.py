from datetime import date
import pytest
from app.actions import ActionItem,track
def test_overdue_action():
 r=track([ActionItem("A1","Send minutes","Sam",date(2026,1,1))],date(2026,1,2))
 assert r["overdue_count"]==1
def test_invalid_status():
 with pytest.raises(ValueError): track([ActionItem("A1","Task","Sam",date(2026,1,1),"unknown")])

from datetime import datetime,timedelta
import pytest
from app.meeting_prep import prepare
def test_meeting_brief():
 r=prepare("Release review",datetime(2026,1,1,10),datetime(2026,1,1,11),["A","B"],["Risks"],[{"source":"doc-1","summary":"Open defects"}])
 assert r["agenda"]==["Risks"] and r["context"][0]["source"]=="doc-1"
def test_invalid_window():
 with pytest.raises(ValueError): prepare("x",datetime(2026,1,1,11),datetime(2026,1,1,10),["A"],["Agenda"])

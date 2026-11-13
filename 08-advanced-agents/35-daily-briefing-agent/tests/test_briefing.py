import pytest
from app.briefing import BriefItem, build_briefing

def test_builds_ordered_source_attributed_sections():
    rows=build_briefing("2026-11-14",[BriefItem("a","tasks","Finish report","task-db",2),BriefItem("b","alerts","Service degraded","monitor",5)])
    assert [s[0] for s in rows.sections] == ["alerts","tasks"]
    assert rows.sections[0][1][0].source == "monitor"

def test_limits_each_section():
    rows=build_briefing("today",[BriefItem(str(i),"updates",f"Update {i}","feed",i%5+1) for i in range(8)],max_per_section=2)
    assert len(rows.sections[0][1]) == 2

def test_rejects_missing_source_and_duplicate_ids():
    with pytest.raises(ValueError): build_briefing("today",[BriefItem("x","tasks","Do","")])
    item=BriefItem("x","tasks","Do","planner")
    with pytest.raises(ValueError): build_briefing("today",[item,item])

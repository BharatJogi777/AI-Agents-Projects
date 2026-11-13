import pytest
from app.outline import Section, build_outline, render_outline

def test_builds_timed_outline():
    sections=[Section("Problem","Explain the problem",5,("src-1",))]
    assert "Audience: Executives" in render_outline("Plan","Executives",sections,total_minutes=10)

def test_rejects_overallocated_timing():
    with pytest.raises(ValueError):
        build_outline("Plan","Team",[Section("A","B",11)],total_minutes=10)

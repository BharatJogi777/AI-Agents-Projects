import pytest
from app.research import Evidence, build_brief, render_brief

def test_brief_keeps_source_and_reports_gaps():
    e=Evidence("s1","Official report","https://example.org","Revenue increased","Table 2")
    brief=build_brief("Market", [e], ["Revenue","Costs"])
    rendered=render_brief(brief)
    assert "s1" in rendered and brief.gaps==("Costs",)

def test_rejects_duplicate_sources():
    e=Evidence("s","T","https://x","C","E")
    with pytest.raises(ValueError):
        build_brief("topic",[e,e])

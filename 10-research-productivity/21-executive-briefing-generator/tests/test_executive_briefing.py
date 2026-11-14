import pytest
from app.executive_briefing import build_briefing

def test_builds_briefing_without_inventing_content():
    result = build_briefing(headline="Q3 status", updates=["Launch delayed"], metrics=["12 open issues"], risks=["Vendor dependency"], decisions_needed=["Approve fallback"], source_labels=["PM report"])
    assert result.key_updates == ("Launch delayed",)
    assert result.source_labels == ("PM report",)

def test_rejects_empty_headline():
    with pytest.raises(ValueError):
        build_briefing(headline=" ", updates=[], metrics=[], risks=[], decisions_needed=[], source_labels=[])

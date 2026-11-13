import pytest
from app.editorial import Draft, EditorialTeam, Finding

def test_research_write_edit_pipeline():
    team = EditorialTeam(
        lambda topic: [Finding("claim", "source:1")],
        lambda topic, findings: Draft("Draft with claim", ("source:1",)),
        lambda draft: draft.text + " Edited",
    )
    result = team.run("topic")
    assert result.edited_text.endswith("Edited")

def test_unknown_citation_rejected():
    team = EditorialTeam(lambda t: [Finding("claim", "source:1")],
                         lambda t, f: Draft("text", ("fake",)), lambda d: d.text)
    with pytest.raises(ValueError): team.run("topic")

def test_empty_research_finding_rejected():
    team = EditorialTeam(lambda t: [Finding("", "source")], lambda t, f: Draft("x", ()), lambda d: d.text)
    with pytest.raises(ValueError): team.run("topic")

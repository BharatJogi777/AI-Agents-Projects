from app.postmortem import draft_postmortem
import pytest

def test_keeps_hypotheses_separate_from_facts():
    result=draft_postmortem(title="API outage",summary="Elevated errors",impact="Checkout degraded",timeline=["10:00 alert"],confirmed_facts=["5xx increased"],hypotheses=["Recent deploy may contribute"],follow_ups=["Review deploy diff"])
    assert result.confirmed_facts!=result.hypotheses

def test_rejects_missing_confirmed_facts():
    with pytest.raises(ValueError): draft_postmortem(title="x",summary="y",impact="z",timeline=["event"],confirmed_facts=[],hypotheses=[],follow_ups=[])

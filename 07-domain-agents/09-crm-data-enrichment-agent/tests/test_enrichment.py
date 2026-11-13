from app.enrichment import propose_enrichment
import pytest

def test_conflicting_low_confidence_value_goes_to_review():
    result=propose_enrichment(field="industry",current_value="Retail",proposed_value="Finance",source="vendor feed",confidence=.8)
    assert result.action=="manual_review_conflict"

def test_rejects_unapproved_field():
    with pytest.raises(ValueError): propose_enrichment(field="password",current_value=None,proposed_value="x",source="feed",confidence=.99)

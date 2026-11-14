import pytest
from app.credibility import assess_source

def test_all_signals_and_no_signals():
    strong = assess_source(**dict.fromkeys(["has_named_author","has_publication_date","is_primary_source","cites_evidence","has_corrections_policy","conflicts_disclosed"], True))
    weak = assess_source(**dict.fromkeys(["has_named_author","has_publication_date","is_primary_source","cites_evidence","has_corrections_policy","conflicts_disclosed"], False))
    assert strong.score == 100 and strong.band == "strong signals"
    assert weak.score == 0 and len(weak.cautions) == 6

def test_rejects_non_boolean():
    with pytest.raises(ValueError):
        assess_source(has_named_author=1, has_publication_date=True, is_primary_source=True, cites_evidence=True, has_corrections_policy=True, conflicts_disclosed=True)

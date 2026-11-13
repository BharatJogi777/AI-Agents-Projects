import pytest
from app.document import Part, assemble_document

def test_assembles_with_provenance_and_review_flags():
    result = assemble_document([Part("p1","text","upload:a","Hello"), Part("p2","image","upload:b","",0.5)])
    assert "[p1:text] Hello" in result.text
    assert result.needs_review == ("p2",)

def test_rejects_duplicate_ids():
    p = Part("x","text","a","one")
    with pytest.raises(ValueError): assemble_document([p,p])

def test_rejects_unknown_media():
    with pytest.raises(ValueError): assemble_document([Part("x","binary","a")])

def test_rejects_missing_source_and_bad_confidence():
    with pytest.raises(ValueError): assemble_document([Part("x","text"," ")])
    with pytest.raises(ValueError): assemble_document([Part("x","text","a",confidence=2)])

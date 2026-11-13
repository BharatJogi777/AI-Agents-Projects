import pytest
from app.citation_eval import evaluate_citations

def test_valid_citation_registry():
    assert evaluate_citations("Claim [src1].",{"src1":"Report"}) == ()

def test_unknown_citation():
    r=evaluate_citations("Claim [missing].",{})
    assert r[0].code == "unknown_citation"

def test_unused_source():
    r=evaluate_citations("No references.",{"src2":"Manual"})
    assert r[0].code == "unused_source"

def test_rejects_blank_source_description():
    with pytest.raises(ValueError): evaluate_citations("x",{"a":" "})

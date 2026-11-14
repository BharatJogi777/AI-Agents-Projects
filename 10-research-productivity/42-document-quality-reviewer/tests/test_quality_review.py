from app.quality_review import review_document
import pytest

def test_flags_missing_section_and_long_line():
    findings=review_document("# Overview\n"+("x"*15),("Risks",),10)
    assert {f.rule for f in findings} >= {"required_section","line_length","final_newline"}

def test_clean_document():
    assert review_document("# Scope\nBody\n",("Scope",),120) == []

def test_invalid_limit_rejected():
    with pytest.raises(ValueError):
        review_document("text",max_line_length=0)

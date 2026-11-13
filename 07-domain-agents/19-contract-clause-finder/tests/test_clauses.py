from app.clauses import find_clauses
import pytest

def test_returns_line_number_and_keyword_evidence():
    result=find_clauses("General terms\nEither party may terminate this agreement.")
    assert result[0].clause_type=="termination" and result[0].line_number==2

def test_rejects_empty_document():
    with pytest.raises(ValueError): find_clauses(" ")

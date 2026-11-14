import pytest
from app.duplicate_knowledge import detect_duplicates

def test_detects_case_and_spacing_duplicates():
    result=detect_duplicates(records=[{"id":"1","text":"Hello, WORLD"},{"id":"2","text":" hello world! "},{"id":"3","text":"different"}])
    assert len(result)==1
    assert result[0].record_ids==("1","2")

def test_rejects_duplicate_ids():
    with pytest.raises(ValueError):
        detect_duplicates(records=[{"id":"x","text":"a"},{"id":"x","text":"b"}])

import pytest
from app.knowledge import Note, search_notes

def test_returns_ranked_source_linked_notes():
    rows=search_notes([Note("n1","Python async event loop"),Note("n2","Python list basics")],"python async")
    assert rows[0].note_id == "n1"
    assert rows[0].score == 2

def test_limit_and_no_match():
    assert len(search_notes([Note("a","alpha"),Note("b","beta")],"alpha",limit=1)) == 1
    assert search_notes([Note("a","alpha")],"unknown") == ()

def test_rejects_bad_input_and_duplicate_ids():
    with pytest.raises(ValueError): search_notes([], " ")
    n=Note("a","text")
    with pytest.raises(ValueError): search_notes([n,n],"text")

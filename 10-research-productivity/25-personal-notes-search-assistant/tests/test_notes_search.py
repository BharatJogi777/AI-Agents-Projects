import pytest
from app.notes_search import search_notes

def test_ranks_notes_by_distinct_keyword_overlap():
    result = search_notes(notes=[{"id":"b","text":"Python memory profiling"}, {"id":"a","text":"Python memory profiling and Python testing"}, {"id":"c","text":"Gardening"}], query="python memory profiling")
    assert result[0].note_id == "a"
    assert result[0].score == 3

def test_rejects_duplicate_note_ids():
    with pytest.raises(ValueError):
        search_notes(notes=[{"id":"x","text":"one"},{"id":"x","text":"two"}], query="one")

def test_rejects_empty_query():
    with pytest.raises(ValueError):
        search_notes(notes=[], query="!!!")

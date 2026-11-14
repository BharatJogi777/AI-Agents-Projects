from app.comparison import compare_documents
import pytest

def test_reports_added_and_removed_lines():
    result=compare_documents("alpha\nbeta","alpha\ngamma")
    assert result["removed_lines"] == 1 and result["added_lines"] == 1
    assert result["changes"][0]["kind"] == "replace"

def test_identical_documents_have_no_changes():
    assert compare_documents("same\ntext","same\ntext")["changes"] == []

def test_empty_document_rejected():
    with pytest.raises(ValueError):
        compare_documents("", "valid")

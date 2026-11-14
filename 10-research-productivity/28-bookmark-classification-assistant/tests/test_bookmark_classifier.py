import pytest
from app.bookmark_classifier import classify_bookmarks

def test_classifies_code_and_unknown_bookmarks():
    result=classify_bookmarks(bookmarks=[{"id":"a","url":"https://github.com/org/repo"},{"id":"b","url":"https://example.org"}])
    assert [x.category for x in result]==["code","other"]

def test_rejects_non_http_url():
    with pytest.raises(ValueError):
        classify_bookmarks(bookmarks=[{"id":"a","url":"file:///tmp/a"}])

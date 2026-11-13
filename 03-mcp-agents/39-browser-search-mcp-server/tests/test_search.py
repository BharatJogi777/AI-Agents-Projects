import pytest
from app.search import normalize_results, validate_query


def test_query_trim():
    assert validate_query(" hello ") == "hello"


def test_query_and_limit_bounds():
    with pytest.raises(ValueError):
        validate_query(" ")
    with pytest.raises(ValueError):
        validate_query("ok", 21)


def test_result_normalization_and_truncation():
    result = normalize_results({"results": [{"title": "x"*400, "url": "https://example.com", "snippet": "s"}]})
    assert len(result[0]["title"]) == 300

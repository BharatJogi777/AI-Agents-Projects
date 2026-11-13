import pytest
from app.prometheus import normalize_result, validate_promql


def test_validate_promql_trims():
    assert validate_promql(" up ") == "up"


def test_rejects_empty_query():
    with pytest.raises(ValueError):
        validate_promql("  ")


def test_normalize_caps_results():
    payload = {"status": "success", "data": {"result": [{"metric": {"job": "api"}, "value": [1, "1"]}]}}
    assert normalize_result(payload)[0]["metric"]["job"] == "api"


def test_backend_error_is_not_silently_accepted():
    with pytest.raises(RuntimeError):
        normalize_result({"status": "error"})

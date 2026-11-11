from datetime import datetime, timezone
import pytest
from app import normalize_tool_result


def test_nested_output_is_json_safe():
    result = normalize_tool_result({"items":[1,2],"at":datetime(2025,1,1,tzinfo=timezone.utc)})
    assert result["ok"] is True
    assert result["data"]["items"] == [1,2]
    assert result["data"]["at"].startswith("2025-01-01")


def test_secrets_are_redacted_recursively():
    result = normalize_tool_result({"token":"abc","nested":{"Authorization":"Bearer x","safe":"yes"}})
    assert result["data"]["token"] == "[REDACTED]"
    assert result["data"]["nested"]["Authorization"] == "[REDACTED]"
    assert result["data"]["nested"]["safe"] == "yes"


def test_circular_reference_and_unsupported_values():
    value = []
    value.append(value)
    normalized = normalize_tool_result({"cycle":value,"object":object()})
    assert normalized["data"]["cycle"][0] == "[CIRCULAR_REFERENCE]"
    assert "unsupported value type" in normalized["warnings"][0]


def test_bounds_are_applied():
    result = normalize_tool_result({"items":list(range(10)),"long":"x"*100},max_items=3,max_string=32)
    assert len(result["data"]["items"]) == 4
    assert result["data"]["items"][-1] == "[7 ITEMS OMITTED]"
    assert "string truncated" in result["warnings"]


def test_total_byte_budget():
    result = normalize_tool_result("x"*2000,max_output_bytes=256)
    assert result["data"]["type"] == "omitted"
    assert "output byte budget exceeded" in result["warnings"]


def test_limits_reject_invalid_values():
    with pytest.raises(ValueError):
        normalize_tool_result({},max_items=0)

from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID

import pytest

from app import normalize_tool_result
from result_normalizer import NormalizationPolicy


def test_nested_output_is_json_safe():
    result = normalize_tool_result({
        "items": [1, 2],
        "at": datetime(2025, 1, 1, tzinfo=timezone.utc),
        "date": date(2025, 1, 2),
        "amount": Decimal("12.50"),
    })
    assert result["ok"] is True
    assert result["data"]["items"] == [1, 2]
    assert result["data"]["at"] == "2025-01-01T00:00:00+00:00"
    assert result["data"]["date"] == "2025-01-02"
    assert result["data"]["amount"] == "12.50"


@pytest.mark.parametrize(
    "key",
    ["token", "Authorization", "api_key", "api-key", "client_secret", "x-api-key", "Cookie"],
)
def test_sensitive_keys_are_redacted_recursively(key):
    result = normalize_tool_result({"nested": {key: "do-not-expose", "safe": "yes"}})
    assert result["data"]["nested"][key] == "[REDACTED]"
    assert result["data"]["nested"]["safe"] == "yes"
    assert "do-not-expose" not in str(result)


def test_secret_value_is_not_traversed():
    secret = {"password": "inside"}
    result = normalize_tool_result({"credentials": secret})
    assert result["data"]["credentials"] == "[REDACTED]"


def test_circular_reference_and_unsupported_values():
    value = []
    value.append(value)
    result = normalize_tool_result({"cycle": value, "object": object()})
    assert result["data"]["cycle"][0] == "[CIRCULAR_REFERENCE]"
    assert any(w.startswith("unsupported value type:") for w in result["warnings"])
    assert result["data"]["object"]["value"] == "[UNSUPPORTED]"


def test_bounds_are_applied():
    result = normalize_tool_result(
        {"items": list(range(10)), "long": "x" * 100},
        max_items=3,
        max_string=32,
    )
    assert len(result["data"]["items"]) == 4
    assert result["data"]["items"][-1] == "[7 ITEMS OMITTED]"
    assert "string truncated" in result["warnings"]


def test_total_byte_budget_returns_compact_envelope():
    result = normalize_tool_result("x" * 2_000, max_output_bytes=256)
    assert result["data"]["type"] == "omitted"
    assert result["warnings"] == ["output byte budget exceeded"]


def test_cycle_detection_allows_shared_non_cyclic_references():
    shared = {"value": 1}
    result = normalize_tool_result([shared, shared])
    assert result["data"] == [{"value": 1}, {"value": 1}]


def test_mapping_non_string_keys_are_not_stringified():
    result = normalize_tool_result({1: "one", "two": 2})
    assert result["data"]["[NON_STRING_KEY_0]"] == "one"
    assert result["data"]["two"] == 2
    assert "non-string mapping key replaced" in result["warnings"]


def test_non_finite_values_are_replaced():
    result = normalize_tool_result({"float": float("nan"), "decimal": Decimal("Infinity")})
    assert result["data"] == {
        "float": "[NON_FINITE_NUMBER]",
        "decimal": "[NON_FINITE_NUMBER]",
    }


def test_bytes_and_uuid_are_handled_without_binary_dump():
    result = normalize_tool_result({
        "binary": b"secret binary",
        "id": UUID("12345678-1234-5678-1234-567812345678"),
    })
    assert result["data"]["binary"] == {"type": "bytes", "length": 13}
    assert result["data"]["id"] == "12345678-1234-5678-1234-567812345678"


def test_ok_flag_must_be_boolean():
    with pytest.raises(TypeError, match="boolean"):
        normalize_tool_result({}, ok="yes")


def test_policy_is_validated_and_conflicting_options_rejected():
    with pytest.raises(ValueError):
        NormalizationPolicy(max_depth=True)
    with pytest.raises(ValueError, match="either policy"):
        normalize_tool_result({}, policy=NormalizationPolicy(), max_items=10)


def test_warning_count_is_bounded():
    result = normalize_tool_result(
        [object() for _ in range(100)],
        policy=NormalizationPolicy(max_warnings=2),
    )
    assert len(result["warnings"]) <= 3
    assert "additional warnings omitted" in result["warnings"]

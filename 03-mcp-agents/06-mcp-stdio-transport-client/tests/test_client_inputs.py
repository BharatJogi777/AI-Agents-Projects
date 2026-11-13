import json
import pytest


def parse_payload(raw):
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("arguments must be a JSON object")
    return value


def test_accepts_object_payload():
    assert parse_payload('{"a": 1}') == {"a": 1}


@pytest.mark.parametrize("raw", ["[]", "null", '"text"', "42"])
def test_rejects_non_object_payload(raw):
    with pytest.raises(ValueError):
        parse_payload(raw)


def test_rejects_malformed_json():
    with pytest.raises(json.JSONDecodeError):
        parse_payload("{")

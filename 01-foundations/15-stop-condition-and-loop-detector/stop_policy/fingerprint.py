"""Canonical, bounded fingerprints for agent state snapshots."""
from __future__ import annotations

import hashlib
import json
import math
from typing import Any


class InvalidAgentState(ValueError):
    """The supplied state cannot safely be fingerprinted."""


def _validate_json_value(value: Any, *, depth: int, max_depth: int,
                         budget: list[int], max_items: int) -> None:
    budget[0] += 1
    if budget[0] > max_items:
        raise InvalidAgentState("state exceeds item limit")
    if depth > max_depth:
        raise InvalidAgentState("state exceeds nesting limit")

    value_type = type(value)
    if value is None or value_type is bool:
        return
    if value_type is int:
        if value.bit_length() > 4096:
            raise InvalidAgentState("integer value exceeds safe limit")
        return
    if value_type is float:
        if not math.isfinite(value):
            raise InvalidAgentState("state contains a non-finite number")
        return
    if value_type is str:
        if len(value) > 100_000:
            raise InvalidAgentState("string value exceeds safe limit")
        return
    if value_type is list or value_type is tuple:
        for item in value:
            _validate_json_value(item, depth=depth + 1, max_depth=max_depth,
                                 budget=budget, max_items=max_items)
        return
    if value_type is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise InvalidAgentState("object keys must be strings")
            if len(key) > 10_000:
                raise InvalidAgentState("object key exceeds safe limit")
            _validate_json_value(item, depth=depth + 1, max_depth=max_depth,
                                 budget=budget, max_items=max_items)
        return
    raise InvalidAgentState("state must contain only JSON-compatible values")


def fingerprint_state(
    state: Any,
    *,
    max_bytes: int = 64_000,
    max_depth: int = 20,
    max_items: int = 10_000,
) -> str:
    """Return a stable SHA-256 fingerprint of a bounded JSON state snapshot.

    Dict keys are canonicalized by JSON serialization. Tuples are accepted as
    JSON arrays. Custom objects, non-string keys, non-finite floats, and
    oversized/deep structures are rejected rather than coerced.
    """
    for name, value, minimum, maximum in (
        ("max_bytes", max_bytes, 128, 1_000_000),
        ("max_depth", max_depth, 1, 100),
        ("max_items", max_items, 1, 100_000),
    ):
        if type(value) is not int or not minimum <= value <= maximum:
            raise ValueError(f"{name} must be an integer in {minimum}..{maximum}")

    _validate_json_value(
        state, depth=0, max_depth=max_depth, budget=[0], max_items=max_items
    )
    try:
        encoded = json.dumps(
            state, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError, RecursionError) as exc:
        raise InvalidAgentState("state cannot be canonically serialized") from exc

    if len(encoded) > max_bytes:
        raise InvalidAgentState("state exceeds fingerprint byte limit")
    return hashlib.sha256(encoded).hexdigest()

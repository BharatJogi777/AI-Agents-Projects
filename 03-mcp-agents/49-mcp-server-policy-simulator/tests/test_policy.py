import pytest

from app.policy import AccessRequest, PolicyEngine, PolicyRule


def engine():
    return PolicyEngine([
        PolicyRule(frozenset({"alice"}), frozenset({"read"}), frozenset({"read:basic"})),
        PolicyRule(frozenset({"alice"}), frozenset({"read"}), effect="deny"),
    ])


def test_explicit_deny_overrides_allow():
    decision = engine().evaluate(AccessRequest("alice", "read", frozenset({"read:basic"})))
    assert not decision.allowed
    assert decision.reason == "explicit_deny"


def test_unknown_principal_denied():
    assert not engine().evaluate(AccessRequest("mallory", "read")).allowed


def test_scope_required():
    policy = PolicyEngine([PolicyRule(frozenset({"alice"}), frozenset({"read"}), frozenset({"read:basic"}))])
    assert not policy.evaluate(AccessRequest("alice", "read")).allowed
    assert policy.evaluate(AccessRequest("alice", "read", frozenset({"read:basic"}))).allowed


def test_invalid_effect_rejected():
    with pytest.raises(ValueError):
        PolicyRule(frozenset({"alice"}), frozenset({"read"}), effect="maybe")

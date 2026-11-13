import pytest
from app.policy import Action, Permission, Policy


def test_policy_checks_exact_tool_action_and_role():
    policy = Policy([Permission("files", Action.READ, frozenset({"reader"}))])
    assert policy.allows(tool="files", action=Action.READ, roles=frozenset({"reader"}))
    assert not policy.allows(tool="files", action=Action.WRITE, roles=frozenset({"reader"}))
    assert not policy.allows(tool="database", action=Action.READ, roles=frozenset({"reader"}))


def test_disabled_rule_denies():
    policy = Policy([Permission("files", Action.DELETE, frozenset({"admin"}), enabled=False)])
    assert not policy.allows(tool="files", action=Action.DELETE, roles=frozenset({"admin"}))


def test_duplicate_rules_rejected():
    rule = Permission("files", Action.READ, frozenset({"reader"}))
    with pytest.raises(ValueError):
        Policy([rule, rule])


def test_empty_roles_rejected():
    with pytest.raises(ValueError):
        Policy([Permission("files", Action.READ, frozenset())])

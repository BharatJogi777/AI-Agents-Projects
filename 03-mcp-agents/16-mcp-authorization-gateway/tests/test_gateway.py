import pytest
from app.gateway import (
    AuthorizationDenied, AuthorizationGateway, Principal, ToolGrant,
)


def gateway(events):
    return AuthorizationGateway(
        {"orders.read": ToolGrant("orders.read", frozenset({"reader", "admin"}))},
        audit=events.append,
    )


def test_authorizes_matching_role_and_audits():
    events = []
    gateway(events).authorize(Principal("user-7", frozenset({"reader"})), "orders.read")
    assert events[-1]["decision"] == "allow"


@pytest.mark.parametrize("principal,tool", [
    (Principal("user", frozenset({"guest"})), "orders.read"),
    (Principal("user", frozenset({"admin"}), active=False), "orders.read"),
    (Principal("user", frozenset({"admin"})), "orders.delete"),
    (Principal("", frozenset({"admin"})), "orders.read"),
])
def test_denies_unknown_inactive_or_unmatched_principal(principal, tool):
    events = []
    with pytest.raises(AuthorizationDenied):
        gateway(events).authorize(principal, tool)
    assert events[-1]["decision"] == "deny"

import pytest
from app.tenancy import Principal, TenantRepository, require_principal

@pytest.fixture
def repo():
    return TenantRepository([
        {"id": "a", "tenant_id": "tenant-a", "value": "A"},
        {"id": "b", "tenant_id": "tenant-b", "value": "B"},
    ])

def test_list_is_tenant_scoped(repo):
    actor = Principal("u1", "tenant-a", frozenset({"reader"}))
    assert [r["id"] for r in repo.list_for(actor)] == ["a"]

def test_cross_tenant_lookup_is_hidden(repo):
    actor = Principal("u1", "tenant-a", frozenset({"reader"}))
    with pytest.raises(LookupError):
        repo.get_for(actor, "b")

def test_missing_principal_fails_closed():
    with pytest.raises(PermissionError):
        require_principal(None)

import pytest
from app.ownership_router import Rule, route_owners

def test_most_specific_rule_wins():
    rules=[Rule("src/",("@team",)),Rule("src/payments/*",("@payments",))]
    assert route_owners(["src/payments/api.py"],rules)["src/payments/api.py"] == ["@payments"]

def test_unowned_path_is_explicit():
    assert route_owners(["docs/a.md"],[]) == {"docs/a.md": []}

def test_rejects_unsafe_path_and_bad_owner():
    with pytest.raises(ValueError): route_owners(["../x"],[])
    with pytest.raises(ValueError): route_owners(["x"],[Rule("x",("team",))])

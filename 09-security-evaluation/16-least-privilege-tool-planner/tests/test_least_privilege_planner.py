import pytest
from app.least_privilege_planner import Tool, plan_tools

def test_selects_minimal_cover():
    result = plan_tools({"read", "search"}, [Tool("combo", frozenset({"read","search"}), 2), Tool("write", frozenset({"write"}), 1)])
    assert result.selected == ("combo",) and result.missing == ()

def test_risk_limit_reports_missing():
    result = plan_tools({"delete"}, [Tool("danger", frozenset({"delete"}), 9)], max_risk=2)
    assert result.missing == ("delete",)

def test_duplicate_names_rejected():
    with pytest.raises(ValueError):
        plan_tools(set(), [Tool("x", frozenset()), Tool("x", frozenset())])

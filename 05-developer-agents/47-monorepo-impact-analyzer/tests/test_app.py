import pytest
from app.monorepo_impact import Component, analyze_impact

def test_propagates_to_dependents():
    cs=[Component("api",("services/api",)), Component("web",("apps/web",),("api",))]
    assert analyze_impact(["services/api/main.py"],cs)["affected"] == ["api","web"]

def test_reports_unmapped_paths():
    assert analyze_impact(["README.md"],[])["unmapped"] == ["README.md"]

def test_rejects_traversal_and_unknown_dependency():
    with pytest.raises(ValueError): analyze_impact(["../secret"],[])
    with pytest.raises(ValueError): analyze_impact([], [Component("a",("a",),("missing",))])

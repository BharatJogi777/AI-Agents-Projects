import pytest
from app.dashboard import build_dashboard_spec, render_spec

def test_builds_constrained_dashboard():
    spec=build_dashboard_spec(metric="revenue",aggregation="sum",dimension="region",time_range="30d",allowed_fields={"revenue","region"})
    assert render_spec(spec)["execution_required"] is True

def test_rejects_unknown_fields_and_aggregation():
    with pytest.raises(ValueError):
        build_dashboard_spec(metric="secret",aggregation="sum",allowed_fields={"revenue"})
    with pytest.raises(ValueError):
        build_dashboard_spec(metric="revenue",aggregation="delete",allowed_fields={"revenue"})

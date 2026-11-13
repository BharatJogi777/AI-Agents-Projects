from app.threat_model import build_threat_model

def test_maps_entry_points_and_controls():
    result = build_threat_model(system_description="support agent", assets=["tickets"], entry_points=["email"])
    assert result["threats"][0]["entry_point"] == "email"
    assert any(x["entry_point"] == "tool boundary" for x in result["threats"])

def test_requires_assets():
    import pytest
    with pytest.raises(ValueError): build_threat_model(system_description="x", assets=[], entry_points=["api"])
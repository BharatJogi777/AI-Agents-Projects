import pytest
from app.exploration import profile_table, suggest_explorations

def test_profiles_missing_numeric_and_categories():
    profiles=profile_table(["age","team"],[[10,"A"],[None,"B"],[30,"A"]])
    assert profiles[0].missing==1 and profiles[0].numeric_max==30
    assert any("missing values" in s for s in suggest_explorations(profiles))

def test_rejects_wrong_width():
    with pytest.raises(ValueError):
        profile_table(["a","b"],[[1]])

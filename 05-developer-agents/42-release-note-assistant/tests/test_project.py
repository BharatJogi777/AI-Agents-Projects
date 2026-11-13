import pytest
from app.release_notes import create_release_notes
def test_filters_internal_for_users():
 out=create_release_notes("2",[{"category":"Added","description":"New endpoint"},{"category":"Fixed","description":"Internal fix","internal_only":True}]); assert "New endpoint" in out and "Internal fix" not in out
def test_rejects_unknown_category():
 with pytest.raises(ValueError): create_release_notes("1",[{"category":"Other","description":"x"}])
def test_audience_validation():
 with pytest.raises(ValueError): create_release_notes("1",[],"everyone")

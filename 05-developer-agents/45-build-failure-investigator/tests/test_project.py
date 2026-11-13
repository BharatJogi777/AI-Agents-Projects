import pytest
from app.build_failure import investigate
def test_classifies_dependency_error():
 r=investigate("ERROR: Could not resolve dependency package"); assert r["primary_category"]=="dependency_resolution"
def test_multiple_categories(): assert len(investigate("permission denied; no space left on device")["findings"])==2
def test_unknown_log(): assert investigate("custom runner output")["primary_category"] is None
def test_empty_log():
 with pytest.raises(ValueError): investigate(" ")

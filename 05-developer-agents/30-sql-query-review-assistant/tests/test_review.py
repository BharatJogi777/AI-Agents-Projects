import pytest
from app.sql_review import review
def test_flags_select_star_and_offset(): assert len(review("SELECT * FROM users OFFSET 100;"))==2
def test_update_without_where(): assert any(x["severity"]=="critical" for x in review("UPDATE users SET active=false"))
def test_empty():
 with pytest.raises(ValueError): review("")

import pytest
from app.conflict_guide import guide
def test_binary_requires_human(): assert guide([{"path":"logo.png","kind":"binary"}])[0]["requires_human_decision"]
def test_content_steps(): assert len(guide([{"path":"app.py"}])[0]["steps"])==3
def test_invalid_kind():
 with pytest.raises(ValueError): guide([{"path":"x","kind":"unknown"}])

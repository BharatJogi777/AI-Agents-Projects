import pytest
from app.commit_message import draft
def test_conventional_message(): assert draft("feat","add search","api")=="feat(api): add search"
def test_breaking_and_body(): assert "feat!: change api" in draft("feat","change api",breaking=True,body="Migration required")
def test_header_limit():
 with pytest.raises(ValueError): draft("feat","x"*80)

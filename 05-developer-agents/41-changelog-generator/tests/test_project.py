import pytest
from app.changelog import generate
def test_groups_and_breaking():
 out=generate(["feat(api): add endpoint","fix: correct timeout","feat!: remove old api"],"1.2"); assert "Features" in out and "BREAKING" in out and "Bug fixes" in out
def test_no_conventional_commits(): assert "No conventional commits" in generate(["misc"],"1")
def test_version_required():
 with pytest.raises(ValueError): generate([],"")

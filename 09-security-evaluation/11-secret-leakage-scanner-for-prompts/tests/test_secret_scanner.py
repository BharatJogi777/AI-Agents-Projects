from app.secret_scanner import scan_prompt

def test_finds_secret_like_assignments():
    result = scan_prompt(prompt="password=hunter2")
    assert result["contains_possible_secret"] and result["count"] == 1

def test_rejects_non_string():
    import pytest
    with pytest.raises(TypeError): scan_prompt(prompt=123)

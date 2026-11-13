from app.onboarding import inspect_repository

def test_inventory_excludes_generated_dirs(tmp_path):
    (tmp_path/"src").mkdir(); (tmp_path/"src"/"main.py").write_text("print('hi')")
    (tmp_path/".git").mkdir(); (tmp_path/".git"/"secret").write_text("x")
    (tmp_path/"pyproject.toml").write_text("[project]")
    result=inspect_repository(tmp_path)
    assert result.files == ("pyproject.toml","src/main.py")
    assert result.entrypoints == ("src/main.py",) and result.manifests == ("pyproject.toml",)

def test_invalid_root_and_limit(tmp_path):
    import pytest
    with pytest.raises(ValueError): inspect_repository(tmp_path/"missing")
    (tmp_path/"a").write_text("a")
    with pytest.raises(ValueError): inspect_repository(tmp_path,max_files=0)

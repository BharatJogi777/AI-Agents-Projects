import pytest
from app.filesystem import ReadOnlyWorkspace

def test_lists_and_reads_files(tmp_path):
    (tmp_path/"a.txt").write_text("hello")
    (tmp_path/"b.txt").write_text("world")
    workspace=ReadOnlyWorkspace(tmp_path)
    assert workspace.list_files()==["a.txt","b.txt"]
    assert workspace.read_text("a.txt")=="hello"

def test_rejects_traversal(tmp_path):
    (tmp_path/"safe.txt").write_text("safe")
    (tmp_path.parent/"outside-mcp.txt").write_text("outside")
    with pytest.raises(PermissionError):
        ReadOnlyWorkspace(tmp_path).read_text("../outside-mcp.txt")

def test_enforces_read_limit(tmp_path):
    (tmp_path/"large.txt").write_text("12345")
    with pytest.raises(ValueError):
        ReadOnlyWorkspace(tmp_path,max_bytes=4).read_text("large.txt")

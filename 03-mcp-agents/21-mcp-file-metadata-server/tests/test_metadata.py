import pytest
from app.metadata import MetadataService

def test_metadata_without_content(tmp_path):
    (tmp_path/"note.txt").write_text("private body")
    item=MetadataService(tmp_path).inspect("note.txt")
    assert item.name=="note.txt" and item.size_bytes==12
    assert not hasattr(item,"content")

def test_rejects_path_escape(tmp_path):
    root=tmp_path/"root"; root.mkdir()
    (tmp_path/"outside.txt").write_text("secret")
    with pytest.raises(PermissionError):
        MetadataService(root).inspect("../outside.txt")

def test_missing_path_fails(tmp_path):
    with pytest.raises(FileNotFoundError):
        MetadataService(tmp_path).inspect("missing")

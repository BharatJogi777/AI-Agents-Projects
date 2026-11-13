from app.architecture import analyze_python_file, analyze_tree

def test_extracts_imports_and_top_level_symbols(tmp_path):
    f=tmp_path/"mod.py"; f.write_text("import os\nfrom pathlib import Path\nclass A: pass\ndef run(): pass\n")
    info=analyze_python_file(f,root=tmp_path)
    assert info.imports == ("os","pathlib")
    assert info.classes == ("A",) and info.functions == ("run",)
    assert len(analyze_tree(tmp_path)) == 1

def test_syntax_error(tmp_path):
    import pytest
    f=tmp_path/"bad.py"; f.write_text("def :")
    with pytest.raises(ValueError): analyze_python_file(f)

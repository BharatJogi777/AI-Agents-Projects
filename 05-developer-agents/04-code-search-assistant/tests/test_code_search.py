from app.code_search import search_code

def test_literal_search_and_limits(tmp_path):
    (tmp_path/"a.py").write_text("hello world\nhello")
    (tmp_path/"b.txt").write_text("hello")
    results=search_code(tmp_path,"hello")
    assert [(m.path,m.line) for m in results] == [("a.py",1),("a.py",2)]
    assert len(search_code(tmp_path,"hello",max_matches=1)) == 1

def test_regex_and_bad_pattern(tmp_path):
    import pytest
    (tmp_path/"a.py").write_text("item_123")
    assert len(search_code(tmp_path,r"item_\d+",regex=True)) == 1
    with pytest.raises(ValueError): search_code(tmp_path,"[",regex=True)

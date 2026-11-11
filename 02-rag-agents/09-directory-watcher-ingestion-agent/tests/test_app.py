from app import DirectoryWatcher
def test_create_modify_delete(tmp_path):
 p=tmp_path/"a.md"; p.write_text("one"); w=DirectoryWatcher(tmp_path)
 assert [x.kind for x in w.scan()]==["created"] and w.scan()==[]
 p.write_text("two"); assert w.scan()[0].kind=="modified"
 p.unlink(); assert w.scan()[0].kind=="deleted"
def test_ignores_extension(tmp_path):
 (tmp_path/"x.exe").write_text("x"); (tmp_path/"a.txt").write_text("a")
 assert [x.path for x in DirectoryWatcher(tmp_path).scan()]==["a.txt"]

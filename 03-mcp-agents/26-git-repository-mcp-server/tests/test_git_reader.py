import subprocess
import pytest
from app.git_reader import GitRepositoryReader

def test_reads_branch_commit_and_status(tmp_path):
    subprocess.run(["git","init",str(tmp_path)],check=True,capture_output=True)
    subprocess.run(["git","-C",str(tmp_path),"config","user.email","test@example.com"],check=True)
    subprocess.run(["git","-C",str(tmp_path),"config","user.name","Test"],check=True)
    (tmp_path/"README.md").write_text("hello")
    subprocess.run(["git","-C",str(tmp_path),"add","README.md"],check=True)
    subprocess.run(["git","-C",str(tmp_path),"commit","-m","initial"],check=True,capture_output=True)
    reader=GitRepositoryReader(tmp_path)
    assert reader.latest_commit()["subject"]=="initial"
    assert isinstance(reader.current_branch(),str)
    assert reader.status()==[]

def test_rejects_non_repository(tmp_path):
    with pytest.raises(ValueError):
        GitRepositoryReader(tmp_path)

import pytest
from app.secure_review import review_source

def test_detects_risky_constructs():
    source = 'eval(user_input)\ndb.execute(f"select * from users where id={uid}")\nsubprocess.run(cmd, shell=True)'
    assert {f.rule for f in review_source(source)} == {"dynamic-execution", "sql-interpolation", "shell-injection"}

def test_clean_source():
    assert review_source("print('safe')") == []

def test_invalid_source():
    with pytest.raises(ValueError):
        review_source("def broken(:")

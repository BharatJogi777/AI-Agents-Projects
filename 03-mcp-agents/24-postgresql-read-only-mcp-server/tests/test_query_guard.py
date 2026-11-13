import pytest
from app.query_guard import validate_read_query

@pytest.mark.parametrize("sql",["SELECT * FROM users","with x as (select 1) select * from x"," select now(); "])
def test_accepts_read_queries(sql):
    assert validate_read_query(sql)

@pytest.mark.parametrize("sql",["DELETE FROM users","SELECT 1; DROP TABLE users","SELECT pg_sleep(10)","SELECT 1 -- comment",""])
def test_rejects_unsafe_queries(sql):
    with pytest.raises((ValueError,PermissionError)):
        validate_read_query(sql)

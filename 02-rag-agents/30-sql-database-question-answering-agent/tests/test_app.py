import sqlite3,pytest
from app import execute_readonly
def db():
 c=sqlite3.connect(":memory:"); c.execute("create table users(id integer,name text)"); c.executemany("insert into users values(?,?)",[(1,"Ada"),(2,"Linus"),(3,"Grace")]); return c
def test_select_and_limit():
 r=execute_readonly(db(),"select id,name from users order by id",{"users"},2); assert r.rows==((1,"Ada"),(2,"Linus")) and r.truncated
def test_write_and_unknown_table_denied():
 c=db()
 with pytest.raises(sqlite3.DatabaseError): execute_readonly(c,"delete from users",{"users"})
 with pytest.raises(sqlite3.DatabaseError): execute_readonly(c,"select * from secrets",{"users"})
def test_only_select():
 with pytest.raises(ValueError): execute_readonly(db(),"pragma table_info(users)",{"users"})
